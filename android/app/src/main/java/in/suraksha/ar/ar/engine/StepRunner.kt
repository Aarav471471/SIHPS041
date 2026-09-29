package in.suraksha.ar.ar.engine

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class StepRunner(
    private val steps: List<StepDefinition>
) {
    private val _currentStepIndex = MutableStateFlow(0)
    val currentStepIndex: StateFlow<Int> = _currentStepIndex.asStateFlow()

    private val _isFinished = MutableStateFlow(false)
    val isFinished: StateFlow<Boolean> = _isFinished.asStateFlow()

    private val results = mutableListOf<StepResult>()
    
    private val startTimeMap = mutableMapOf<String, Long>()
    private val attemptsMap = mutableMapOf<String, Int>()
    private val mistakesMap = mutableMapOf<String, MutableList<String>>()

    fun start() {
        if (steps.isEmpty()) return
        _currentStepIndex.value = 0
        markStepStart(steps[0].id)
    }

    private fun markStepStart(stepId: String) {
        startTimeMap[stepId] = System.currentTimeMillis()
        if (!attemptsMap.containsKey(stepId)) {
            attemptsMap[stepId] = 0
            mistakesMap[stepId] = mutableListOf()
        }
    }

    fun recordMistake(mistakeDetail: String) {
        val currentStep = steps[_currentStepIndex.value].id
        mistakesMap[currentStep]?.add(mistakeDetail)
        attemptsMap[currentStep] = (attemptsMap[currentStep] ?: 0) + 1
    }

    fun completeCurrentStep(points: Int) {
        val currentStep = steps[_currentStepIndex.value]
        val duration = System.currentTimeMillis() - (startTimeMap[currentStep.id] ?: System.currentTimeMillis())
        
        results.add(
            StepResult(
                stepId = currentStep.id,
                points = points,
                maxPoints = currentStep.maxPoints,
                attempts = attemptsMap[currentStep.id] ?: 0,
                durationMs = duration,
                mistakes = mistakesMap[currentStep.id]?.toList() ?: emptyList()
            )
        )

        if (_currentStepIndex.value < steps.size - 1) {
            _currentStepIndex.value += 1
            markStepStart(steps[_currentStepIndex.value].id)
        } else {
            _isFinished.value = true
        }
    }

    fun getResults(): List<StepResult> = results.toList()
}
