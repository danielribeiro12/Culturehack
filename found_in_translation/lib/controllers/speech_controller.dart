// speech_controller.dart
import 'package:record/record.dart';
import 'package:http/http.dart' as http;

class SpeechController {
  final _audioRecorder = Record();
  bool _isListening = false;
  String _text = '';

  Future<void> initSpeech() async {
    // Initialize recorder permissions
    await _audioRecorder.hasPermission();
  }

  Future<void> startListening() async {
    await _audioRecorder.start();
    _isListening = true;
    _text = 'Listening...';
  }

  Future<void> stopListening() async {
    final path = await _audioRecorder.stop();
    _isListening = false;

    if (path != null) {
      final request = http.MultipartRequest(
          'POST', Uri.parse('http://localhost:5000/translate-audio'));

      request.files.add(await http.MultipartFile.fromPath('audio', path));
      request.fields['target_lang'] = 'es';

      final response = await request.send();
      _text = await response.stream.bytesToString();
    }
  }

  // Getters
  bool get isListening => _isListening;
  String get text => _text;
}
