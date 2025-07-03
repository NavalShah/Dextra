# Dextra - Hand Gesture Recognition System

A real-time hand gesture recognition system that uses MediaPipe for hand detection and custom-trained neural networks to classify both static hand gestures and dynamic finger movements. The system achieves high accuracy (~95%) while maintaining real-time performance suitable for interactive applications.

## Features

- **Real-time Hand Detection**: Leverages MediaPipe's robust hand tracking to detect up to 2 hands simultaneously
- **Dual Classification System**:
  - Static gesture recognition (5 gestures)
  - Dynamic movement classification (4 motion patterns)
- **Interactive Data Collection**: Built-in modes for collecting training data
- **Lightweight Models**: TensorFlow Lite models optimized for edge deployment
- **Visual Feedback**: Real-time visualization of hand landmarks and gesture classifications

## System Architecture

### Hand Detection Pipeline

The system uses MediaPipe's hand detection model to extract 21 3D landmarks from each detected hand. These landmarks represent key points on the hand including:

- Wrist (landmark 0)
- Thumb joints (landmarks 1-4)
- Index finger joints (landmarks 5-8)
- Middle finger joints (landmarks 9-12)
- Ring finger joints (landmarks 13-16)
- Pinky joints (landmarks 17-20)

### Pointer Mechanism

The pointer functionality is triggered when the system detects a "Pointer" gesture (class 2). When activated:

1. The system tracks the index fingertip position (landmark 8)
2. A history of the last 16 positions is maintained in a deque
3. The movement trajectory is analyzed by the point history classifier
4. Visual feedback shows the pointer trail with increasing circle sizes

### Model Architecture

#### 1. Static Gesture Classifier

- **Input**: 42 normalized landmark coordinates (21 points � 2D)
- **Architecture**:
  ```
  Input(42) � Dropout(0.2) � Dense(20, ReLU) � Dropout(0.4) � Dense(10, ReLU) � Dense(5, Softmax)
  ```
- **Output Classes**:
  - 0: Open (open palm)
  - 1: Close (closed fist)
  - 2: Pointer (index finger extended)
  - 3: OK (thumb and index forming circle)
  - 4: Peace Sign (index and middle fingers extended)

#### 2. Dynamic Movement Classifier

- **Input**: 32 values representing 16 consecutive movement vectors
- **Architecture**:
  ```
  Input(32) � Dropout(0.2) � Dense(24, ReLU) � Dropout(0.5) � Dense(10, ReLU) � Dense(4, Softmax)
  ```
- **Output Classes**:
  - 0: Stop (no significant movement)
  - 1: Clockwise (circular clockwise motion)
  - 2: Counter Clockwise (circular counter-clockwise motion)
  - 3: Move (linear directional movement)

### Data Preprocessing

1. **Landmark Normalization**:

   - Coordinates are converted to relative positions from the wrist (landmark 0)
   - Values are normalized by the maximum absolute value to ensure scale invariance
   - This makes the system robust to different hand sizes and distances from camera

2. **Movement History Processing**:
   - Raw pixel coordinates are converted to relative movements
   - Normalized by image dimensions for resolution independence
   - Maintains temporal context through a sliding window approach

## Usage

### Basic Operation

```bash
python app.py
```

### Command Line Arguments

- `--device`: Camera device index (default: 0)
- `--width`: Capture width in pixels (default: 960)
- `--height`: Capture height in pixels (default: 540)
- `--min_detection_confidence`: Minimum confidence for hand detection (default: 0.7)
- `--min_tracking_confidence`: Minimum confidence for hand tracking (default: 0.5)

### Keyboard Controls

- **ESC**: Exit the application
- **n**: Normal mode (inference only)
- **k**: Keypoint logging mode (collect static gesture data)
- **h**: History logging mode (collect movement data)
- **0-9**: Class label for data collection modes

### Data Collection

1. **Collecting Static Gestures** (Mode 1):

   - Press 'k' to enter keypoint logging mode
   - Make the desired hand gesture
   - Press the corresponding number (0-4) to save the sample
   - Data is appended to `model/keypoint_classifier/keypoint.csv`

2. **Collecting Movement Patterns** (Mode 2):
   - Press 'h' to enter history logging mode
   - Make the pointer gesture to start tracking
   - Perform the desired movement pattern
   - Press the corresponding number (0-3) to save the sample
   - Data is appended to `model/point_history_classifier/point_history.csv`

## Training Custom Models

### Prerequisites

```bash
pip install tensorflow numpy pandas scikit-learn
```

### Training Process

1. **Static Gesture Model**:

   ```bash
   jupyter notebook keypoint_classification.ipynb
   ```

   - Modify gesture labels in `keypoint_classifier_label.csv`
   - Collect training data using mode 1
   - Run the notebook to train and export the model

2. **Movement Pattern Model**:
   ```bash
   jupyter notebook point_history_classification.ipynb
   ```
   - Modify movement labels in `point_history_classifier_label.csv`
   - Collect training data using mode 2
   - Run the notebook to train and export the model

## Technical Details

### Performance Optimizations

- **TensorFlow Lite**: Models are converted to TFLite format for efficient inference
- **Preprocessing Cache**: Landmark normalization is vectorized using NumPy
- **Deque Structure**: Fixed-size queue for O(1) append operations
- **Single-threaded Inference**: Reduces overhead for lightweight models

### Coordinate System

- MediaPipe provides normalized coordinates (0-1 range)
- Converted to pixel coordinates for visualization
- Pointer tracking uses pixel coordinates for precise control
- Movement classification uses normalized deltas for scale invariance

### Confidence Thresholds

- Hand detection: 0.7 (adjustable via CLI)
- Hand tracking: 0.5 (adjustable via CLI)
- Movement classification: 0.5 (hardcoded in PointHistoryClassifier)

## Potential Applications

1. **Gesture-Based Control Systems**: Control smart home devices, presentations, or media players
2. **Sign Language Recognition**: Extend the gesture vocabulary for basic sign language
3. **Virtual Mouse/Pointer**: Use hand movements for touchless computer interaction
4. **Gaming Interface**: Create gesture-based controls for games
5. **Accessibility Tools**: Provide alternative input methods for users with mobility limitations
6. **AR/VR Interaction**: Natural hand gesture input for immersive environments

## Future Enhancements

- Support for more complex gestures and combinations
- Two-hand gesture recognition
- Gesture sequence recognition for commands
- Integration with voice commands
- Export to mobile platforms (Android/iOS)
- Real-time gesture customization without retraining

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- TensorFlow/TensorFlow Lite
- NumPy

## License

This project is open source and available under the MIT License.

## Acknowledgments

- MediaPipe team for the excellent hand tracking solution
- TensorFlow team for the machine learning framework
- OpenCV community for computer vision tools
