// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.jetbrains.kotlin.android) apply false
}

// true // Needed to make the file non-empty and valid
// Removed the 'true' as it's not necessary for a non-empty .kts file when plugins are declared.
