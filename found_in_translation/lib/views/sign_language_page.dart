import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:camera/camera.dart';

class SignLanguagePage extends StatefulWidget {
  const SignLanguagePage({super.key});

  @override
  State<SignLanguagePage> createState() => _SignLanguagePageState();
}

class _SignLanguagePageState extends State<SignLanguagePage> {
  CameraController? _controller;
  bool _isCameraInitialized = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    if (cameras.isEmpty) return;

    _controller = CameraController(cameras[0], ResolutionPreset.medium);
    try {
      await _controller!.initialize();
      if (mounted) {
        setState(() => _isCameraInitialized = true);
      }
    } catch (e) {
      debugPrint('Error initializing camera: $e');
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sign Language Page'),
      ),
      body: Stack(
        children: [
          if (_isCameraInitialized && _controller != null)
            CameraPreview(_controller!)
          else
            Container(
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage('assets/background2.jpg'),
                  fit: BoxFit.cover,
                ),
              ),
            ),
          const Center(
            child: Text(
              'Sign Language Page Content',
              style: TextStyle(fontSize: 24, color: Colors.white),
            ),
          ),
          Positioned(
            bottom: 20,
            left: 20,
            right: 20,
            child: ElevatedButton(
              onPressed: () async {
                if (_controller != null && _controller!.value.isInitialized) {
                  try {
                    final image = await _controller!.takePicture();
                    // Handle the captured image here
                    debugPrint('Image captured: ${image.path}');
                  } catch (e) {
                    debugPrint('Error capturing image: $e');
                  }
                }
              },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 15),
                backgroundColor: Colors.blue,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              child: const Text(
                'Capture',
                style: TextStyle(fontSize: 18, color: Colors.white),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
