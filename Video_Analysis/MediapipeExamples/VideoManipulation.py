import cv2
import mediapipe as mp
import datetime
import numpy as np



class VideoManipulation:
    
  def __init__(self, input = 1, ouput_path = "DATA\\", mode = "pose", background = "black"):
    self.cap = cv2.VideoCapture(input)
    self.datetime = datetime.datetime.now()
    self.background = background
    self.filename = self.datetime.ctime().replace(":", "_").replace(" ", "_")
    fps = self.cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(self.cap.get(3))
    frame_height = int(self.cap.get(4))
    size = (frame_width, frame_height)
    self.result = cv2.VideoWriter(self.filename, 
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            fps, size)
    if mode == "pose":
      self.getpose()
    elif mode == "mesh":
      self.getMesh()
    elif mode == "holistic":
      self.getHolistic() 
      
      
      
  def getHolistic(self):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic
    with mp_holistic.Holistic( 
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as holistic:
      while self.cap.isOpened():
        success, image = self.cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
          break
    self.cap.release()

  def getMesh(self):
    
    # For webcam input:
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    # For webcam input:
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
      while self.cap.isOpened():
        success, image = self.cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style())
        # Flip the image horizontally for a selfie-view display.
        self.result.write(image)
        cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
          break
      self.result.release()
      cap.release()
      
  def getpose(self):
    
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    blank_image = np.zeros((int(self.cap.get(4)),int(self.cap.get(3)),3), np.uint8)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
      while self.cap.isOpened():
        success, image = self.cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      
        if self.background == "black":
          blank_image = np.zeros((int(self.cap.get(4)),int(self.cap.get(3)),3), np.uint8)
          mp_drawing.draw_landmarks(
              blank_image,
              results.pose_landmarks,
              mp_pose.POSE_CONNECTIONS,
              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        else: 
                  mp_drawing.draw_landmarks(
              image,
              results.pose_landmarks,
              mp_pose.POSE_CONNECTIONS,
              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        self.result.write(blank_image)
        if self.background == "black":
          cv2.imshow('MediaPipe Pose', cv2.flip(blank_image, 1))
        else: 
          cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
          break
      self.cap.release()
      self.result.release()
  
makeVid = VideoManipulation(background="none")

