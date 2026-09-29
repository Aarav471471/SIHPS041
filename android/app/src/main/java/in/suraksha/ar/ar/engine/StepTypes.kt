package in.suraksha.ar.ar.engine

sealed class StepType {
    object Intro : StepType()
    object FindTargets : StepType()
    object SelectItem : StepType()
    object OrderSequence : StepType()
    object ActionSequence : StepType()
    object WalkPath : StepType()
    object ReadGauge : StepType()
    object CheckpointQuiz : StepType()
    object Summary : StepType()
}

data class StepDefinition(
    val id: String,
    val type: String,
    val titleKey: String,
    val instructionKey: String,
    val audioKey: String,
    val maxPoints: Int,
    val params: Map<String, Any>? = null
)

data class StepResult(
    val stepId: String,
    val points: Int,
    val maxPoints: Int,
    val attempts: Int,
    val durationMs: Long,
    val mistakes: List<String>
)
