import React, { createContext, useContext, useRef, useState, useCallback } from 'react'
import { stableHash } from '../../utils/hash'

const DeduplicationContext = createContext(null)

/**
 * Provider to track rendered content and prevent duplication.
 * Scoped to a specific rendering context (e.g., inside AstrologyProfile).
 */
export const DeduplicationProvider = ({ children, onDuplicateDetected }) => {
    // We use a ref for the Set to modify it synchronously during render
    // This is technically a side effect during render, but necessary for immediate 
    // duplicate detection within the same render pass.
    const renderedHashes = useRef(new Set())

    // Track warnings to log them once per render cycle if needed, 
    // avoiding console spam during re-renders
    const warningsThisRender = useRef([])

    // Reset function to clear history (e.g., when switching house systems completely)
    const reset = useCallback(() => {
        renderedHashes.current.clear()
        warningsThisRender.current = []
    }, [])

    const isRendered = useCallback((text) => {
        if (!text) return false
        const hash = stableHash(text)
        return renderedHashes.current.has(hash)
    }, [])

    const trackContent = useCallback((text) => {
        if (!text) return
        const hash = stableHash(text)

        if (renderedHashes.current.has(hash)) {
            // Duplicate detected!
            // Log internally as requested
            const msg = `[AstrologyRenderer] Duplicate content detected (hash: ${hash}): "${text.substring(0, 30)}..."`

            // Only log if we haven't logged this specific warning recently (simple throttling)
            // For now, simpler: just push to internal log array or console.debug
            console.debug(msg)

            if (onDuplicateDetected) {
                onDuplicateDetected(text, hash)
            }
            return false // Indicates it was a duplicate
        }

        renderedHashes.current.add(hash)
        return true // Indicates it was new
    }, [onDuplicateDetected])

    return (
        <DeduplicationContext.Provider value={{ isRendered, trackContent, reset }}>
            {children}
        </DeduplicationContext.Provider>
    )
}

export const useDeduplication = () => {
    const context = useContext(DeduplicationContext)
    if (!context) {
        throw new Error('useDeduplication must be used within a DeduplicationProvider')
    }
    return context
}
