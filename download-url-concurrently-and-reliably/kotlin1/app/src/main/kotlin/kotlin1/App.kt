package kotlin1

import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.request.*
import io.ktor.client.statement.HttpResponse
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun main() {
    // processSimple()
    processUrlReliably(32000, 624, "https://httpbin.org/status/400")
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

fun processUrlReliably(timeout: Long, retry_delay: Long, url: String) = runBlocking {
    val client = HttpClient(CIO) {
        expectSuccess = true
    }

    try {
        withTimeout(timeout) {
            download(client, url)
            .retry { ex ->
                (ex is ClientRequestException).also {
                    if (it) {
                        delay(retry_delay)
                        print(".")
                    }
                }
            }
            .collect { println("+") }  // should never happen
        }
    } catch (e: TimeoutCancellationException) {
        println("Global timeout exceeded!\n${e}")
    }
}

fun download(client: HttpClient, url: String): Flow<HttpResponse> = flow {
    emit(client.get(url))
}
