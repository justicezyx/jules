package com.example.aichatapp.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.aichatapp.data.ChatMessage // Updated import
import com.example.aichatapp.data.SenderType // Updated import
import com.example.aichatapp.ui.theme.AIChatAppTheme

@Composable
fun MessageBubble(message: ChatMessage) {
    val bubbleColor = if (message.sender == SenderType.USER) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant // Changed AI bubble color
    val textColor = if (message.sender == SenderType.USER) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant // Changed AI text color
    val alignment = if (message.sender == SenderType.USER) Alignment.End else Alignment.Start

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 4.dp),
        horizontalAlignment = alignment
    ) {
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = bubbleColor),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp) // Added elevation
        ) {
            Box(modifier = Modifier.widthIn(max = LocalConfiguration.current.screenWidthDp.dp * 0.8f)) { // Added maxWidth
                Text(
                    text = message.text,
                    modifier = Modifier.padding(12.dp),
                    color = textColor
                )
            }
        }
    }
}
                modifier = Modifier.padding(12.dp),
                color = textColor
            )
        }
    }
}

@Preview(showBackground = true, name = "User Message Preview")
@Composable
fun UserMessageBubblePreview() {
    AIChatAppTheme {
        MessageBubble(message = ChatMessage("This is a test message from the user. It's a bit longer to check wrapping.", SenderType.USER))
    }
}

@Preview(showBackground = true, name = "AI Message Preview")
@Composable
fun AiMessageBubblePreview() {
    AIChatAppTheme {
        MessageBubble(message = ChatMessage("This is a response from the AI. It's also a bit longer to see how it wraps.", SenderType.AI))
    }
}
