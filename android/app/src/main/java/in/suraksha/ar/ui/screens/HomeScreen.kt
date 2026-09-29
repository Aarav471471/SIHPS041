package in.suraksha.ar.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onNavigateToAr: (String) -> Unit,
    onNavigateToCertificates: () -> Unit
) {
    val modules = listOf(
        "fire" to "Fire & Explosion Response",
        "gas" to "Gas Leak & Confined Space",
        "machinery" to "Machinery Safety (Lite)",
        "electrical" to "Electrical Safety (Lite)",
        "ppe" to "PPE & Height (Lite)"
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Training Modules") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onNavigateToCertificates) {
                Text("Certs")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(modules) { (id, title) ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onNavigateToAr(id) },
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(text = title, style = MaterialTheme.typography.titleMedium)
                        Button(onClick = { onNavigateToAr(id) }) {
                            Text("Start AR")
                        }
                    }
                }
            }
        }
    }
}
