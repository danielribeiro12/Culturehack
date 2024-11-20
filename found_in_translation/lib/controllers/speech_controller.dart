import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SpeechController extends ChangeNotifier {
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool _isListening = false;
  String _text = '';
  String _translatedText = '';

  Future<void> initSpeech() async {
    try {
      _isListening = await _speech.initialize();
    } catch (e) {
      _text = 'Error initializing: $e';
    }
  }

  Future<void> startListening() async {
    if (!_isListening) {
      _isListening = await _speech.listen(
        onResult: (result) async {
          _text = result.recognizedWords;
          if (_text.isNotEmpty) {
            await _translateToMalay();
          }
          notifyListeners();
        },
      );
      notifyListeners();
    }
  }

  Future<void> stopListening() async {
    await _speech.stop();
    _isListening = false;

    // Send text to backend for processing
    if (_text.isNotEmpty) {
      try {
        final response = await http.get(
          Uri.parse('http://localhost:5000/translate-text').replace(
            queryParameters: {
              'text': _text,
              'from_lang': 'en',
              'to_lang': 'ko',
            },
          ),
        );

        if (response.statusCode == 200) {
          _text = response.body;
        } else {
          _text = 'Error: ${response.statusCode}';
        }
      } catch (e) {
        _text = 'Network error: $e';
      }
    }

    notifyListeners();
  }

  Future<void> _translateToMalay() async {
    try {
      print('Attempting to translate: $_text'); // Debug log

      // Try using IP address instead of localhost
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/translate-text').replace(
          queryParameters: {
            'text': _text,
            'from_lang': 'en',
            'to_lang': 'ms',
          },
        ),
      );

      print('Response status: ${response.statusCode}'); // Debug log
      print('Response body: ${response.body}'); // Debug log

      if (response.statusCode == 200) {
        _translatedText = response.body;
      } else {
        _translatedText = 'Error: ${response.statusCode}';
      }
    } catch (e) {
      print('Detailed error: $e'); // Debug log
      _translatedText = 'Network error: $e';
    }
    notifyListeners();
  }

  bool get isListening => _isListening;
  String get text => _text;
  String get translatedText => _translatedText;
}
