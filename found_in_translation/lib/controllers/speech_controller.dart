// speech_controller.dart
import 'package:record/record.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SpeechController {
  final _audioRecorder = Record();
  bool _isListening = false;
  String _text = '';

  Future<void> initSpeech() async {
    try {
      final hasPermission = await _audioRecorder.hasPermission();
      if (!hasPermission) {
        _text = 'Microphone permission denied';
        return;
      }
    } catch (e) {
      _text = 'Error initializing: $e';
    }
  }

  Future<void> startListening() async {
    try {
      await _audioRecorder.start(
        encoder: AudioEncoder.aacLc, // Use AAC encoding
        bitRate: 128000, // 128kbps
        samplingRate: 44100, // 44.1kHz
      );
      _isListening = true;
      _text = 'Recording...';
    } catch (e) {
      _text = 'Error recording: $e';
      _isListening = false;
    }
  }

  Future<void> stopListening() async {
    try {
      final path = await _audioRecorder.stop();
      _isListening = false;
      _text = 'Processing...';

      if (path != null) {
        // Create multipart request
        final request = http.MultipartRequest(
          'POST',
          Uri.parse('http://localhost:5000/process-audio'),
        );

        // Add the audio file
        request.files.add(
          await http.MultipartFile.fromPath('audio', path),
        );

        // Add language parameters
        request.fields['from_lang'] = 'en';
        request.fields['to_lang'] = 'es';

        // Send the request
        final streamedResponse = await request.send();
        final response = await http.Response.fromStream(streamedResponse);

        if (response.statusCode == 200) {
          final jsonResponse = jsonDecode(response.body);
          _text = jsonResponse['translation'];
        } else {
          _text = 'Error: ${response.statusCode}';
        }
      }
    } catch (e) {
      _text = 'Error processing: $e';
    }
  }

  // Getters
  bool get isListening => _isListening;
  String get text => _text;
}
