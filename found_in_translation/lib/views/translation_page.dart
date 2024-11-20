import 'package:flutter/material.dart';
import '../controllers/speech_controller.dart';

class TranslationPage extends StatefulWidget {
  const TranslationPage({super.key});

  @override
  _TranslationPageState createState() => _TranslationPageState();
}

class _TranslationPageState extends State<TranslationPage> {
  late SpeechController _speechController;

  @override
  void initState() {
    super.initState();
    _speechController = SpeechController();
    _speechController.initSpeech();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Translation Page'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                if (_speechController.isListening) {
                  _speechController.stopListening();
                } else {
                  _speechController.startListening();
                }
                setState(() {});
              },
              child: Text(_speechController.isListening
                  ? 'Stop Listening'
                  : 'Start Listening'),
            ),
            const SizedBox(height: 20),
            Text(
              _speechController.text,
              style: const TextStyle(fontSize: 24),
            ),
          ],
        ),
      ),
    );
  }
}
