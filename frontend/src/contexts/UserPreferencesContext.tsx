import React, { createContext, useEffect } from 'react'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ExpansionStates {
    [key: string]: boolean | undefined
}

interface UserPreferencesState {
    language: string
    houseSystemView: 'whole_sign' | 'placidus'
    detailLevel: 'overview' | 'full'
    theme: 'dark' | 'light'
    expansionStates: {
        whole_sign: ExpansionStates
        placidus: ExpansionStates
        [key: string]: ExpansionStates
    }
}

interface UserPreferencesActions {
    setLanguage: (lang: string) => void
    setHouseSystemView: (view: 'whole_sign' | 'placidus') => void
    setDetailLevel: (level: 'overview' | 'full') => void
    setTheme: (theme: 'dark' | 'light') => void
    toggleExpansion: (houseSystem: string, id: string, isExpanded?: boolean) => void
    getExpansionState: (houseSystem: string, id: string, defaultState: boolean) => boolean
}

type UserPreferencesStore = UserPreferencesState & UserPreferencesActions

const usePreferencesStore = create<UserPreferencesStore>()(
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
                        [id]: isExpanded !== undefined ? isExpanded : !state.expansionStates[houseSystem]?.[id]
                    }
                }
            })),

            getExpansionState: (_houseSystem, _id, defaultState) => {
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

const UserPreferencesContext = createContext<UserPreferencesStore | null>(null)

interface UserPreferencesProviderProps {
    children: React.ReactNode
}

export const UserPreferencesProvider: React.FC<UserPreferencesProviderProps> = ({ children }) => {
    const store = usePreferencesStore() as UserPreferencesStore

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

export function useUserPreferences(): UserPreferencesStore;
export function useUserPreferences<T>(selector: (state: UserPreferencesStore) => T): T;
export function useUserPreferences<T>(selector?: (state: UserPreferencesStore) => T) {
    // Note: This pattern of using the context provider simply to wrap the zustand store 
    // is a bit redundant if we are just using the global hook, but it keeps the pattern consistent.
    // However, Zustand is designed to be used directly. The original code used both.
    // Since the original code had `const store = usePreferencesStore()` inside the provider, the provider basically just exposes the store state.
    
    // To maintain compatibility with existing usage like `useUserPreferences()` returning the whole store:
    if (selector) {
        return usePreferencesStore(selector)
    }
    return usePreferencesStore()
}

// Helper to get expansion state with fallback
export const useExpansionState = (houseSystem: string, id: string, defaultState: boolean): [boolean, (newState?: boolean) => void] => {
    const expansionStates = usePreferencesStore(state => state.expansionStates)
    const toggleExpansion = usePreferencesStore(state => state.toggleExpansion)

    // If specific state exists, use it. Otherwise use default.
    // We check for undefined because false is a valid state (collapsed)
    const isExpanded = expansionStates[houseSystem]?.[id] !== undefined
        ? expansionStates[houseSystem][id]!
        : defaultState

    const toggle = (newState?: boolean) => {
        toggleExpansion(houseSystem, id, newState !== undefined ? newState : !isExpanded)
    }

    return [isExpanded, toggle]
}
