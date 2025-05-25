package com.example.aichatapp.data

// Data models
data class ChatMessage(
    val text: String,
    val sender: SenderType,
    val timestamp: Long = System.currentTimeMillis()
)

enum class SenderType {
    USER, AI
}
