/**
 * Generates a 32-bit FNV-1a hash for a given string.
 * Used for stable content deduplication.
 * 
 * @param {string} str - The input string to hash
 * @returns {number} - The 32-bit hash value
 */
export const stableHash = (str: string): number => {
    if (!str) return 0

    // Clean string: remove extra whitespace to ensure similar sentences match
    const cleanStr = str.trim().replace(/\s+/g, ' ')

    let hash = 2166136261
    const len = cleanStr.length

    for (let i = 0; i < len; i++) {
        hash ^= cleanStr.charCodeAt(i)
        // 32-bit integer multiplication
        hash = Math.imul(hash, 16777619)
    }

    return hash >>> 0 // Convert to unsigned 32-bit integer
}
