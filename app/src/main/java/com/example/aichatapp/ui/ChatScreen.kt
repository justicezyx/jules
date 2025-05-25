package com.example.aichatapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.aichatapp.ui.theme.AIChatAppTheme
import com.example.aichatapp.data.ChatMessage
import com.example.aichatapp.data.SenderType
import com.example.aichatapp.viewmodel.ChatViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    viewModel: ChatViewModel = viewModel()
) {
    val messages by viewModel.messages.collectAsStateWithLifecycle()
    var currentText by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("AI Chat") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            MessageList(
                messages = messages,
                modifier = Modifier.weight(1f)
            )
            MessageInput(
                currentText = currentText,
                onTextChanged = { currentText = it },
                onMessageSend = {
                    if (it.isNotBlank()) {
                        viewModel.sendMessage(it)
                        currentText = ""
                    }
                }
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ChatScreenPreview() {
    AIChatAppTheme {
        // For preview, we can't use a real ViewModel easily without Hilt or other DI.
        // So, we'll display it with an empty message list or a mock/fake ViewModel if needed.
        // For this basic preview, an empty ChatScreen (which will show the initial AI message) is fine.
         ChatScreen(viewModel = PreviewChatViewModel()) // Using a simple preview ViewModel
    }
}

// A simple ViewModel for Preview purposes
class PreviewChatViewModel : ChatViewModel() {
    init {
        // Override the init block or messages for preview if needed
        // For instance, to show a specific set of messages:
        // _messages.value = listOf(
        // ChatMessage("Preview: Hello User!", SenderType.USER),
        // ChatMessage("Preview: Hello AI!", SenderType.AI)
        // )
    }
    // You can override methods if they do complex things not suitable for preview
}
