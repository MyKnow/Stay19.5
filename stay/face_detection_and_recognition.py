import numpy as np
import cv2 as cv
import sys
import os
import requests
from django.conf import settings

detect_onnx_file = os.path.join(settings.STAY_APP_DIR, 'ai_model', 'face_detection_yunet_2022mar.onnx')
recognize_onnx_file = os.path.join(settings.STAY_APP_DIR, 'ai_model', 'face_recognition_sface_2021dec.onnx')

''' 
    Function <get_valid_faces> 

        ** Parameter : faces, input_img
            -> 사진에서 감지된 모든 얼굴 정보, 업로드된 이미지
        Model : OpenCV FaceRecognizerSF
        0. Initialize Face Recognizer model
        1. Extract features of currently interested faces
        2. Calculate L2 Norm, Cosine Similarity
        3. Examine similarity
            - Same identity detected : No need to compare once more
            - Diff identity detected : Keep comparing till the end
        4. Return Value : The list of unique facial information
'''


# Compare faces in the image and Return only unique face embeddings
def get_valid_faces(faces, input_img):
    # The list containing numpy.ndarray
    valid_faces = []

    # *** [initialize_FaceRecognizerSF] ***
    recognizer = cv.FaceRecognizerSF.create(recognize_onnx_file, "")
    # Threshold for examine similarity
    cosine_similarity_threshold = 0.263
    l2_similarity_threshold = 1.128

    # List to contain Same face indices
    same_face_indicies = []
    id = []
    # Compare faces by faces
    for i in range(len(faces)):
        # If currently pointing face has already been detected as
        # the same identity, just skip comparison
        if i in same_face_indicies:
            continue
        face_standard_align = recognizer.alignCrop(input_img, faces[i])
        face_standard_feature = recognizer.feature(face_standard_align)
        for j in range(i + 1, len(faces)):
            # If comparing face has already been detected as
            # the same identity, just skip comparison
            if j in same_face_indicies:
                continue
            # Align the face and extract features
            face_subject_align = recognizer.alignCrop(input_img, faces[j])
            face_subject_feature = recognizer.feature(face_subject_align)

            # Get scores to judge similarity
            cosine_score = recognizer.match(face_standard_feature, face_subject_feature, cv.FaceRecognizerSF_FR_COSINE)
            l2_score = recognizer.match(face_standard_feature, face_subject_feature, cv.FaceRecognizerSF_FR_NORM_L2)

            # If given scores exceed the threshold, "Same identity"
            # Unless, "Other identity"
            print("[Scores for Comparison]")
            print(
                "-------------------------------------------------------------------------------------------------------------------------------------")
            print("** Explanation **")
            print("Cosine Similarity : (Higher value -> Higher similarity, max 1.0)")
            print("Norm L2 Similarity : (Lower value -> Higher similarity, min 0.0)")
            print(
                "-------------------------------------------------------------------------------------------------------------------------------------")
            if (cosine_score >= cosine_similarity_threshold) or (l2_score <= l2_similarity_threshold):
                print('They have the same identity. Cosine Similarity: {}, threshold: {}'.format(cosine_score,
                                                                                                 cosine_similarity_threshold))
                print('They have the same identity. NormL2 Distance: {}, threshold: {}\n'.format(l2_score,
                                                                                                 l2_similarity_threshold))
                # Make sure this face(index) not to be compared in the future comparisons
                same_face_indicies.append(j)
            else:
                print('They have other identities. Cosine Similarity: {}, threshold: {}'.format(cosine_score,
                                                                                                cosine_similarity_threshold))
                print('They have other identities. NormL2 Distance: {}, threshold: {}\n'.format(l2_score,
                                                                                                l2_similarity_threshold))
        id.append(i)
        valid_faces.append(faces[i])
    print("\nThe number of detected Faces :", len(valid_faces))
    print()
    return valid_faces


''' 
    Function <detect_faces_in_img> 

        ** Parameter : Uploaded image (cv.imread 거친 이미지)
        Model : OpenCV FaceDetectorYN
        0. Initialize Face Detector model
        1. Detect faces in image
        2. Remove duplicated faces and leave unique information
        3. Return Value : The list of facial information in the image
'''


# Receive facial embeddings of people in image
def detect_faces_in_img(input_img):
    ''' [initialize_FaceDetectorYN] '''

    detector = cv.FaceDetectorYN_create(
        detect_onnx_file,
        "",
        (320, 320),
        0.9,
        0.3,
        5000
    )

    ''' [initialize_FaceDetectorYN] '''

    # Make sure the image for detection is found
    if input_img is not None:
        # Get input image width and height. Then, resize it
        input_img_width = int(input_img.shape[1] * 1.0)  # scale
        input_img_height = int(input_img.shape[0] * 1.0)  # scale
        input_img = cv.resize(input_img, (input_img_width, input_img_height))

        ''' ***** [inference] ***** '''

        # Set input size before inference
        detector.setInputSize((input_img_width, input_img_height))
        faces = detector.detect(input_img)

        # [Exception Handling]
        # If no faces are detected, error notice is printed
        assert faces[1] is not None, "Cannot find a face in the input image"

        # Remove duplicated faces and just leave unique embeddings
        # valid_faces : The list holds unique face embeddings
        detected_valid_faces = get_valid_faces(faces[1], input_img)

        ''' ***** [inference] ***** '''

        return detected_valid_faces


''' 
    Function <compare_with_other_images> 

        ** Assumption : 1 image and corresponding labels and facial information are imported
        ** Parameter : db_img, db_faces, db_labels, input_img, input_faces, labels_and_faces
            -> DB에서 불러온 이미지, 얼굴 정보, 레이블, 업로드된 이미지, 얼굴 정보, 레이블과 얼굴 정보 쌍들의 리스트
        1. Receive features using recognizer (AlignCrop & Extracting Features)
        2. Examine the similarities between pointed faces (Loop is necessary)
            1) Same Identity -> Grant label and stop comparison
            2) Diff Identities -> Change the target to the next face
        3. Return Value : The list of pairs of granted label and facial information
                [[granted_label1, facial info1], [granted_label2, facial_info2], ...]
        4. Expected result : Store these data to the database
'''

# 1. image_addresses    == db_img
# 2. people_i_values    == db_faces
# 3. people_i_number    == db_labels
# 4. image_url          == input_img
# 5. results            == input_faces
# 6. labels_and_faces   == labels_and_faces

# labels_and_faces = [ [label, face_info], [label, face_info], [label, face_info], ... ]

def compare_with_other_images(db_img_url, db_faces, db_labels, image_url, input_faces, new_labels):
    # Read image through OpenCV Library (Img to Numpy Array)
    ''' Uploaded image '''
    response = requests.get(image_url, stream=True).raw
    input_img = np.asarray(bytearray(response.read()), dtype=np.uint8)
    input_img = cv.imdecode(input_img, cv.IMREAD_COLOR)
    ''' DB image '''
    response = requests.get(db_img_url, stream=True).raw
    db_img = np.asarray(bytearray(response.read()), dtype=np.uint8)
    db_img = cv.imdecode(db_img, cv.IMREAD_COLOR)
    # *** [initialize_FaceRecognizerSF] ***
    recognizer = cv.FaceRecognizerSF.create(recognize_onnx_file, "")

    # Threshold for examine similarity
    cosine_similarity_threshold = 0.263
    l2_similarity_threshold = 1.128

    for i in range(len(input_faces)):
        # Label to be granted
        granted_label = -1
        # If label has already been granted..
        if new_labels[i] != -1:
            continue
        input_face = np.array(input_faces[i])
        input_face_align = recognizer.alignCrop(input_img, input_face)
        input_face_feature = recognizer.feature(input_face_align)
        for j in range(len(db_faces)):
            db_face = np.array(db_faces[j])
            db_face_align = recognizer.alignCrop(db_img, db_face)
            db_face_feature = recognizer.feature(db_face_align)

            # Get scores to judge similarity
            cosine_score = recognizer.match(input_face_feature, db_face_feature, cv.FaceRecognizerSF_FR_COSINE)
            l2_score = recognizer.match(input_face_feature, db_face_feature, cv.FaceRecognizerSF_FR_NORM_L2)

            print("[Scores for Comparison]")
            print("-------------------------------------------------------------------------------------------------------------------------------------")
            print("** Explanation **")
            print("Cosine Similarity : (Higher value -> Higher similarity, max 1.0)")
            print("Norm L2 Similarity : (Lower value -> Higher similarity, min 0.0)")
            print("-------------------------------------------------------------------------------------------------------------------------------------")
            if (cosine_score >= cosine_similarity_threshold) or (l2_score <= l2_similarity_threshold):
                print('They have the same identity. Cosine Similarity: {}, threshold: {}'.format(cosine_score,
                                                                                                 cosine_similarity_threshold))
                print('They have the same identity. NormL2 Distance: {}, threshold: {}\n'.format(l2_score,
                                                                                                 l2_similarity_threshold))
                # Make sure this face(index) not to be compared in the future comparisons
                granted_label = db_labels[j]
                break
            else:
                print('They have other identities. Cosine Similarity: {}, threshold: {}'.format(cosine_score,
                                                                                                cosine_similarity_threshold))
                print('They have other identities. NormL2 Distance: {}, threshold: {}\n'.format(l2_score,
                                                                                                l2_similarity_threshold))
        # granted_label = db_labels[j] : Same identity is detected
        # granted_label = -1           : New identity
        new_labels[i] = granted_label
    return new_labels


''' 
    Function <facial_recognition_model> 

        ** Parameter : the path of new image & pairs of label and facial information
        0. Initialize all variables
        1. Read uploaded new image
        2. Detection & Recognition
        3. Return Value : newly granted labels and face information included in new image
'''


def facial_recognition_model(img_url, loaded_faces=None):
    ''' 1. Read uploaded new image '''
    # Bring input image
    response = requests.get(img_url, stream=True).raw
    input_img = np.asarray(bytearray(response.read()), dtype=np.uint8)
    input_img = cv.imdecode(input_img, cv.IMREAD_COLOR)

    ''' 2. Detection & Recognition '''
    # Uploaded image has not been detected
    if input_img is None:
        # No images in database
        if loaded_faces is None:
            sys.exit("*** No images from database ***")
        # No uploaded image, but images exist in database
        else:
            sys.exit("*** No input image to compare ***")
    # Uploaded image exists
    else:
        # Detecting faces in uploaded image
        # Type : list (containing all detected faces -> Type : numpy.ndarray)
        input_faces = detect_faces_in_img(input_img)

    return input_faces

