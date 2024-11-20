import 'package:camera/camera.dart';

class CameraService {
  CameraController? controller;
  List<CameraDescription> cameras = [];

  Future<void> initialize() async {
    cameras = await availableCameras();
    if (cameras.isEmpty) return;

    controller = CameraController(
      cameras[0],
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await controller?.initialize();
  }

  void dispose() {
    controller?.dispose();
  }
}
