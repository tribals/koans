import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertEquals


class TruthTest {
    @Test fun test_truth() {
        assertFalse(true)
    }
    @Test fun test_numbers() {
        val n = 42
        assertEquals(n, 42)
    }
}
