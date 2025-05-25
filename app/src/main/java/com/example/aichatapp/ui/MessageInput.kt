package com.example.aichatapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color // Keep if TextFieldDefaults uses it.
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.aichatapp.ui.theme.AIChatAppTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MessageInput(
    currentText: String,
    onTextChanged: (String) -> Unit,
    onMessageSend: (String) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp), // Adjusted padding
        verticalAlignment = Alignment.CenterVertically
    ) {
        TextField(
            value = currentText,
            onValueChange = onTextChanged,
            modifier = Modifier.weight(1f),
            placeholder = { Text("Type a message") },
            colors = TextFieldDefaults.textFieldColors(
                 // Let's use default indicator colors for better theme adherence, or remove if not needed
                // focusedIndicatorColor = Color.Transparent, // Removed for default behavior
                // unfocusedIndicatorColor = Color.Transparent // Removed for default behavior
            ),
            shape = MaterialTheme.shapes.medium,
            singleLine = true // Optional: for better single line input behavior
        )
        Spacer(modifier = Modifier.width(8.dp))
        IconButton(
            onClick = { onMessageSend(currentText) },
            enabled = currentText.isNotBlank()
        ) {
            Icon(
                imageVector = Icons.Filled.Send,
                contentDescription = "Send message",
                tint = if (currentText.isNotBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f) // Icon tint based on enabled state
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MessageInputPreview() {
    var text by remember { mutableStateOf("") }
    AIChatAppTheme {
        MessageInput(
            currentText = text,
            onTextChanged = { text = it },
            onMessageSend = { /* Do nothing in preview */ }
        )
    }
}

@Preview(showBackground = true)
@Composable
fun MessageInputPreview_WithText() {
    var text by remember { mutableStateOf("Hello there!") }
    AIChatAppTheme {
        MessageInput(
            currentText = text,
            onTextChanged = { text = it },
            onMessageSend = { /* Do nothing in preview */ }
        )
    }
}
