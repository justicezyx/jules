package com.example.aichatapp.ui

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.aichatapp.data.ChatMessage // Updated import
import com.example.aichatapp.data.SenderType // Updated import
import com.example.aichatapp.ui.theme.AIChatAppTheme

@Composable
fun MessageList(
    messages: List<ChatMessage>,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()

    // Scroll to bottom when new messages are added
    LaunchedEffect(messages) {
        if (messages.isNotEmpty()) {
            // We are using reverseLayout and messages.reversed(), so index 0 is the newest.
            listState.animateScrollToItem(0)
        }
    }

    LazyColumn(
        state = listState,
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(8.dp),
        reverseLayout = true // To show latest messages at the bottom
    ) {
        items(messages.reversed()) { message -> // Display messages in correct order
            MessageBubble(message = message)
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MessageListPreview() {
    AIChatAppTheme {
        val previewMessages = listOf(
            ChatMessage("Hello there!", SenderType.USER, System.currentTimeMillis() - 2000),
            ChatMessage("Hi! How can I help you?", SenderType.AI, System.currentTimeMillis() - 1000),
            ChatMessage("This is a test message.", SenderType.USER, System.currentTimeMillis())
        )
        MessageList(messages = previewMessages)
    }
}
