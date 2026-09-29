package in.suraksha.ar.ar.scenes

import in.suraksha.ar.ar.engine.StepDefinition
import io.github.sceneview.ar.ArSceneView
import io.github.sceneview.ar.node.ArModelNode
import io.github.sceneview.math.Position
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch

interface SceneBuilder {
    fun buildScene(sceneView: ArSceneView, step: StepDefinition, onInteraction: (String) -> Unit)
    fun clearScene(sceneView: ArSceneView)
}

class FireSceneBuilder : SceneBuilder {
    private val activeNodes = mutableListOf<ArModelNode>()

    override fun buildScene(sceneView: ArSceneView, step: StepDefinition, onInteraction: (String) -> Unit) {
        when (step.type) {
            "FIND_TARGETS" -> {
                // Load Exit Signs
                val exitSign = ArModelNode(sceneView.engine).apply {
                    loadModelGlbAsync(glbFileLocation = "content/models/exit_sign.glb")
                    position = Position(x = 0.0f, y = 0.0f, z = -1.5f) // 1.5m in front of camera
                    onTap = { _, _ -> onInteraction("exit_sign_tapped") }
                }
                sceneView.addChild(exitSign)
                activeNodes.add(exitSign)
            }
            "ACTION_SEQUENCE" -> {
                // Load Fire Flames
                val fire = ArModelNode(sceneView.engine).apply {
                    loadModelGlbAsync(glbFileLocation = "content/models/fire_flames.glb")
                    position = Position(x = 0.0f, y = -0.5f, z = -2.0f)
                }
                
                // Load Extinguisher
                val extinguisher = ArModelNode(sceneView.engine).apply {
                    loadModelGlbAsync(glbFileLocation = "content/models/extinguisher_co2.glb")
                    position = Position(x = 0.5f, y = -0.5f, z = -1.0f)
                    onTap = { _, _ -> onInteraction("extinguisher_tapped") }
                }
                
                sceneView.addChild(fire)
                sceneView.addChild(extinguisher)
                activeNodes.add(fire)
                activeNodes.add(extinguisher)
            }
        }
    }

    override fun clearScene(sceneView: ArSceneView) {
        activeNodes.forEach { 
            sceneView.removeChild(it)
            it.destroy() 
        }
        activeNodes.clear()
    }
}

class GasSceneBuilder : SceneBuilder {
    private val activeNodes = mutableListOf<ArModelNode>()

    override fun buildScene(sceneView: ArSceneView, step: StepDefinition, onInteraction: (String) -> Unit) {
        when (step.type) {
            "READ_GAUGE" -> {
                val monitor = ArModelNode(sceneView.engine).apply {
                    loadModelGlbAsync(glbFileLocation = "content/models/gas_monitor.glb")
                    position = Position(x = 0.0f, y = -0.2f, z = -0.5f) // Close to screen
                }
                sceneView.addChild(monitor)
                activeNodes.add(monitor)
            }
            "FIND_ZONES" -> {
                val cloud = ArModelNode(sceneView.engine).apply {
                    loadModelGlbAsync(glbFileLocation = "content/models/gas_cloud.glb")
                    position = Position(x = -1.0f, y = 0.0f, z = -2.0f)
                    onTap = { _, _ -> onInteraction("gas_cloud_detected") }
                }
                sceneView.addChild(cloud)
                activeNodes.add(cloud)
            }
        }
    }

    override fun clearScene(sceneView: ArSceneView) {
        activeNodes.forEach { 
            sceneView.removeChild(it)
            it.destroy() 
        }
        activeNodes.clear()
    }
}

