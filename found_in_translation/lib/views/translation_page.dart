import 'package:flutter/material.dart';
import '../controllers/speech_controller.dart';
import 'package:provider/provider.dart';

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
        title: const Text('Speech to Text'),
      ),
      body: ListenableBuilder(
        listenable: _speechController,
        builder: (context, child) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () async {
                    if (_speechController.isListening) {
                      await _speechController.stopListening();
                    } else {
                      await _speechController.startListening();
                    }
                  },
                  child: Icon(
                    _speechController.isListening ? Icons.mic_off : Icons.mic,
                    size: 30,
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  'English: ${_speechController.text}',
                  style: const TextStyle(fontSize: 24),
                ),
                const SizedBox(height: 20),
                Text(
                  'Malay: ${_speechController.translatedText}',
                  style: const TextStyle(fontSize: 24),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
