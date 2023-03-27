package kotlin1

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.statement.HttpResponse
// import io.ktor.http.*

fun main() {
    processUrlRebustly(32000, 624, "https://httpbin.org/status/400")
    // processSimple()
}

// fun processSimple() = runBlocking {
//     simple()
//     .retry() { ex -> (ex is Exception)}
//     .collect { value -> println(value) }
// }

// fun simple(): Flow<Int> = flow { // flow builder
//     for (i in 1..3) {
//         delay(1000)
//         if (i % 2 == 0) {
//             throw Exception("oops!")
//         } else {
//             emit(i)
//         }
//     }
// }

fun processUrlRebustly(timeout: Long, retry_delay: Long, url: String) = runBlocking {
    val client = HttpClient(CIO) {
        expectSuccess = true
    }

    try {
        withTimeout(timeout) {
            download(client, url)
            .retry { ex ->
                (ex is ClientRequestException).also { if (it) delay(retry_delay) }
            }
            .collect()
        }
    } catch (e: TimeoutCancellationException) {
        println("Global timeout exceeded!")
    }
}

fun download(client: HttpClient, url: String): Flow<HttpResponse> = flow {
    val resp = client.get<HttpResponse>(url)
    emit(resp)
}
