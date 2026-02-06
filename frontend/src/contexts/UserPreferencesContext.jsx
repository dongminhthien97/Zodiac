import React, { createContext, useContext, useEffect } from 'react'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const usePreferencesStore = create(
    persist(
        (set) => ({
            language: 'vi',
            houseSystemView: 'whole_sign', // Default view, will be overridden by API meta availability
            detailLevel: 'overview', // 'overview' | 'full'
            theme: 'dark',

            setLanguage: (lang) => set({ language: lang }),
            setHouseSystemView: (view) => set({ houseSystemView: view }),
            setDetailLevel: (level) => set({ detailLevel: level }),
            setTheme: (theme) => set({ theme }),

            // Store expansion states for house systems separately
            // Structure: { whole_sign: { 'sectionId-layerId': boolean }, placidus: { ... } }
            expansionStates: { whole_sign: {}, placidus: {} },

            toggleExpansion: (houseSystem, id, isExpanded) => set((state) => ({
                expansionStates: {
                    ...state.expansionStates,
                    [houseSystem]: {
                        ...state.expansionStates[houseSystem],
                        [id]: isExpanded
                    }
                }
            })),

            getExpansionState: (houseSystem, id, defaultState) => {
                // This is a helper, but since we can't access state inside state definition easily for return,
                // we'll implement the logic in the hook wrapper or component.
                return defaultState
            }
        }),
        {
            name: 'user-preferences',
        }
    )
)

const UserPreferencesContext = createContext(null)

export const UserPreferencesProvider = ({ children }) => {
    const store = usePreferencesStore()

    // Sync theme with HTML root
    useEffect(() => {
        const root = window.document.documentElement
        root.classList.remove('light', 'dark')
        root.classList.add(store.theme)
    }, [store.theme])

    return (
        <UserPreferencesContext.Provider value={store}>
            {children}
        </UserPreferencesContext.Provider>
    )
}

export const useUserPreferences = () => {
    const store = usePreferencesStore()
    if (!store) {
        throw new Error('useUserPreferences must be used within UserPreferencesProvider')
    }
    return store
}

// Helper to get expansion state with fallback
export const useExpansionState = (houseSystem, id, defaultState) => {
    const expansionStates = useUserPreferences(state => state.expansionStates)
    const toggleExpansion = useUserPreferences(state => state.toggleExpansion)

    // If specific state exists, use it. Otherwise use default.
    // We check for undefined because false is a valid state (collapsed)
    const isExpanded = expansionStates[houseSystem]?.[id] !== undefined
        ? expansionStates[houseSystem][id]
        : defaultState

    const toggle = (newState) => {
        toggleExpansion(houseSystem, id, newState !== undefined ? newState : !isExpanded)
    }

    return [isExpanded, toggle]
}
