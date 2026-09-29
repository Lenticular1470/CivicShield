from pathlib import Path
from urllib.request import urlretrieve

import cv2


BASE_DIR = Path(__file__).resolve().parent
FACES_DIR = BASE_DIR / "faces"
MODELS_DIR = BASE_DIR / "models" / "face_recognition"
MODEL_URLS = {
    "yunet.onnx": "https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "sface.onnx": "https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
}
COSINE_THRESHOLD = 0.363


def ensure_model(filename):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / filename
    if not model_path.exists():
        temporary_path = model_path.with_suffix(".download")
        print(f"Downloading face model: {filename}")
        try:
            urlretrieve(MODEL_URLS[filename], temporary_path)
            temporary_path.replace(model_path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
    return str(model_path)


def detect_faces(detector, image):
    height, width = image.shape[:2]
    detector.setInputSize((width, height))
    _, faces = detector.detect(image)
    return faces


def load_known_faces(detector, recognizer):
    FACES_DIR.mkdir(parents=True, exist_ok=True)
    known_features = []
    known_names = []

    for image_path in sorted(FACES_DIR.iterdir()):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Could not read face image: {image_path.name}")
            continue

        faces = detect_faces(detector, image)
        if faces is None or len(faces) == 0:
            print(f"No face found in: {image_path.name}")
            continue

        largest_face = max(faces, key=lambda face: face[2] * face[3])
        aligned_face = recognizer.alignCrop(image, largest_face)
        known_features.append(recognizer.feature(aligned_face))
        known_names.append(image_path.stem)

    return known_features, known_names


def main():
    if not hasattr(cv2, "FaceDetectorYN") or not hasattr(cv2, "FaceRecognizerSF"):
        print("OpenCV face APIs are missing. Install opencv-contrib-python from requirements.txt.")
        return

    yunet_path = ensure_model("yunet.onnx")
    sface_path = ensure_model("sface.onnx")
    detector = cv2.FaceDetectorYN.create(yunet_path, "", (320, 320))
    recognizer = cv2.FaceRecognizerSF.create(sface_path, "")
    known_features, known_names = load_known_faces(detector, recognizer)

    if not known_features:
        print("No usable face images found in the faces folder. Add a clear JPG, JPEG, or PNG photo.")

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open camera 0.")
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            faces = detect_faces(detector, frame)
            if faces is not None:
                for face in faces:
                    x, y, width, height = face[:4].astype(int)
                    aligned_face = recognizer.alignCrop(frame, face)
                    feature = recognizer.feature(aligned_face)

                    best_score = -1.0
                    best_index = -1
                    for index, known_feature in enumerate(known_features):
                        score = recognizer.match(
                            feature,
                            known_feature,
                            cv2.FaceRecognizerSF_FR_COSINE,
                        )
                        if score > best_score:
                            best_score = score
                            best_index = index

                    if best_score >= COSINE_THRESHOLD:
                        name = known_names[best_index]
                        color = (0, 255, 0)
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)
                        print("Unknown person detected!")

                    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                    cv2.putText(
                        frame,
                        name,
                        (x, max(y - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        color,
                        2,
                    )

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
