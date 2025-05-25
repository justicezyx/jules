package com.example.aichatapp.viewmodel

import app.cash.turbine.test
import com.example.aichatapp.data.SenderType
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TestWatcher // Using TestWatcher for Main dispatcher for older setup
import org.junit.runner.Description // Using TestWatcher for Main dispatcher for older setup
import kotlinx.coroutines.Dispatchers // For older setup
import kotlinx.coroutines.test.TestCoroutineDispatcher // For older setup
import kotlinx.coroutines.test.resetMain // For older setup
import kotlinx.coroutines.test.setMain // For older setup
import androidx.arch.core.executor.testing.InstantTaskExecutorRule


@OptIn(ExperimentalCoroutinesApi::class)
class ChatViewModelTest {

    // Rule to make LiveData updates instantaneous, good for general ViewModel testing
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    // TestCoroutineDispatcher for more control if needed, though runTest often suffices
    // For viewModelScope, runTest's dispatcher is usually enough.
    // If we were injecting dispatchers, we'd inject a testDispatcher.
    // private val testDispatcher = StandardTestDispatcher() // For newer coroutines-test
    private val testDispatcher = TestCoroutineDispatcher() // For older coroutines-test

    private lateinit var viewModel: ChatViewModel

    @Before
    fun setUp() {
        // Dispatchers.setMain(testDispatcher) // Set main dispatcher for tests
        // For kotlinx-coroutines-test 1.6.0+ `runTest` handles this.
        // If using an older version, the above line is crucial.
        // Let's assume runTest handles it, if not, this might be needed.
        viewModel = ChatViewModel() // MockAiService is instantiated directly in ChatViewModel
    }

    // @After // Not strictly needed with runTest's dispatcher if it replaces Main.
    // fun tearDown() {
    //    Dispatchers.resetMain() // Reset main dispatcher
    //    testDispatcher.cleanupTestCoroutines()
    // }

    @Test
    fun `initialMessages_containsWelcomeMessageFromAI`() = runTest {
        viewModel.messages.test {
            val firstEmission = awaitItem()
            assertEquals(1, firstEmission.size)
            assertEquals(SenderType.AI, firstEmission[0].sender)
            assertTrue("Initial message should be from AI", firstEmission[0].text.contains("Hello! I'm your AI assistant."))
            // cancelAndIgnoreRemainingEvents() // Use if further events are not expected or relevant
            // For this test, we only care about the first emission.
            // However, if the flow remains active and could emit more, cleanup is good.
            // Since other tests might send messages, it's better to ensure this test is isolated.
            // If `sendMessage` is called elsewhere, this flow could see more items.
            // For a simple initial state test, this is often enough.
            // Let's refine by ensuring no other emissions are processed by this test block.
            cancelAndConsumeRemainingEvents() // More robust
        }
    }

    @Test
    fun `sendMessage_whenUserSaysHello_addsUserMessageAndAIReply`() = runTest {
        viewModel.messages.test {
            // 1. Initial AI welcome message
            val initialItems = awaitItem()
            assertEquals(1, initialItems.size)
            assertEquals(SenderType.AI, initialItems.first().sender)
            assertTrue(initialItems.first().text.contains("Hello! I'm your AI assistant."))

            viewModel.sendMessage("Hello")

            // 2. User message "Hello" should be added
            val itemsAfterUserMessage = awaitItem()
            assertEquals(2, itemsAfterUserMessage.size)
            assertEquals("Hello", itemsAfterUserMessage.last().text)
            assertEquals(SenderType.USER, itemsAfterUserMessage.last().sender)

            // 3. AI response to "Hello"
            // runTest's virtual time dispatcher handles delays in MockAiService and ChatViewModel
            val itemsAfterAIResponse = awaitItem()
            assertEquals(3, itemsAfterAIResponse.size)
            assertEquals("Hi there! How can I assist you today?", itemsAfterAIResponse.last().text)
            assertEquals(SenderType.AI, itemsAfterAIResponse.last().sender)

            cancelAndConsumeRemainingEvents() // Ensure no other events interfere
        }
    }

    @Test
    fun `sendMessage_whenUserAsksHowAreYou_addsUserMessageAndAIReply`() = runTest {
        viewModel.messages.test {
            awaitItem() // Consume initial AI message

            viewModel.sendMessage("How are you?")

            // User message
            val itemsAfterUserMessage = awaitItem()
            assertEquals(2, itemsAfterUserMessage.size)
            assertEquals("How are you?", itemsAfterUserMessage.last().text)
            assertEquals(SenderType.USER, itemsAfterUserMessage.last().sender)

            // AI response
            val itemsAfterAIResponse = awaitItem()
            assertEquals(3, itemsAfterAIResponse.size)
            assertEquals("I'm doing well, thank you for asking!", itemsAfterAIResponse.last().text)
            assertEquals(SenderType.AI, itemsAfterAIResponse.last().sender)

            cancelAndConsumeRemainingEvents()
        }
    }

    @Test
    fun `sendMessage_whenUserInputIsBlank_doesNotAddMessage`() = runTest {
         viewModel.messages.test {
            val initialMessages = awaitItem() // Consume initial AI message
            assertEquals(1, initialMessages.size)

            viewModel.sendMessage("   ") // Send blank message

            // After sending a blank message, no new messages should be added.
            // The flow should not emit a new list or if it does, it should be identical to initialMessages.
            // We can assert that no new item is emitted within a certain timeout,
            // or check the current value of the ViewModel's list directly if appropriate.

            // Since sendMessage for a blank string doesn't modify _messages,
            // no new emission should happen. Turbine's expectNoEvents is good here.
            expectNoEvents() // This will wait for a brief period (default 1s) to ensure no events.

            // As an additional check, verify the underlying list in the ViewModel
            val currentMessages = viewModel.messages.value
            assertEquals("Message list size should remain unchanged after blank input", initialMessages.size, currentMessages.size)
            assertEquals("Content of messages should be identical to initial messages", initialMessages, currentMessages)

            // No need to cancelAndConsumeRemainingEvents if expectNoEvents() is used and passes,
            // but if it's not used, or to be safe:
            // cancelAndConsumeRemainingEvents()
            // However, if expectNoEvents passes, it implies the flow is quiet.
        }
    }
}
