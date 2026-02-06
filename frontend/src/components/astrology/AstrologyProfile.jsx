import React, { useEffect, useState, useMemo } from 'react'
import { DeduplicationProvider } from './DeduplicationProvider'
import SectionRenderer from './SectionRenderer'
import HouseSystemToggle from './HouseSystemToggle'
import { validateContent } from '../../utils/contentValidator'
import { SECTION_ORDER } from '../../constants/sections'
import { useUserPreferences } from '../../contexts/UserPreferencesContext'
import { AlertCircle } from 'lucide-react'

const AstrologyProfile = ({ contentJson }) => {
    const [validationResult, setValidationResult] = useState({ isValid: true, errors: [] })
    const { houseSystemView, setHouseSystemView } = useUserPreferences()

    // Validation on mount or data change
    useEffect(() => {
        const result = validateContent(contentJson)
        setValidationResult(result)

        if (!result.isValid) {
            console.error('Astrology Profile Content Validation Failed:', result.errors)
        }

        // Initialize house system selection based on availability
        if (result.isValid && contentJson.meta) {
            const available = contentJson.meta.house_system_used

            if (available === 'whole_sign') setHouseSystemView('whole_sign')
            else if (available === 'placidus') setHouseSystemView('placidus')
            // if 'both', keep current user preference, or default to whole_sign if not set (handled by default state)
        }
    }, [contentJson, setHouseSystemView])

    // Scroll restoration logic
    const handleHouseSystemSwitch = (newSystem) => {
        // Capture current scroll position relative to the document
        const scrollY = window.scrollY

        setHouseSystemView(newSystem)

        // Restore scroll after render (useEffect or requestAnimationFrame)
        // React's flushSync could also be used if instant layout effect is needed, 
        // but browser's built-in scroll restoration usually handles position preservation 
        // if the height doesn't change drastically.
        // If we wanted to be very precise, we'd find the currently viewed element and scroll to it.
        // For now, maintain simple position.
        requestAnimationFrame(() => {
            window.scrollTo(0, scrollY)
        })
    }

    if (!validationResult.isValid) {
        return (
            <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/20 text-red-200">
                <div className="flex items-center gap-3 mb-2">
                    <AlertCircle />
                    <h3 className="font-bold">Cannot render astrology profile</h3>
                </div>
                <ul className="list-disc pl-5 text-sm opacity-80">
                    {validationResult.errors.map((err, i) => <li key={i}>{err}</li>)}
                </ul>
            </div>
        )
    }

    const { sections, meta } = contentJson

    return (
        <div className="astrology-profile-container max-w-4xl mx-auto py-8 px-4 sm:px-0">

            {/* House System Toggle */}
            <HouseSystemToggle
                availableSystems={meta.house_system_used}
                currentSystem={houseSystemView}
                onSwitch={handleHouseSystemSwitch}
            />

            {/* Main Content Area - Wrapped in Deduplication Provider */}
            {/* Critical: Keying the provider by houseSystemView ensures that 
          the deduplication cache is reset when switching systems, 
          preventing hash collisions across systems if content overlaps logically but shouldn't visually. 
          However, the user requirement says: "If both... Do not cross-render sentences". 
          Resetting the provider achieves this naturally. 
      */}
            <DeduplicationProvider key={houseSystemView}>
                <div className="space-y-2">
                    {SECTION_ORDER.map(sectionKey => {
                        // Special handling for house_interpretation
                        if (sectionKey === 'house_interpretation') {
                            const houseData = sections.house_interpretation
                            if (!houseData) return null

                            // Get data for current selected system
                            // The API schema says house_interpretation has keys 'whole_sign' and 'placidus'
                            const activeSystemData = houseData[houseSystemView]
                            if (!activeSystemData) return null // handle graceful missing data

                            return (
                                <SectionRenderer
                                    key={sectionKey}
                                    sectionKey={sectionKey}
                                    sectionData={activeSystemData}
                                    houseSystemContext={houseSystemView}
                                />
                            )
                        }

                        // Normal sections
                        return (
                            <SectionRenderer
                                key={sectionKey}
                                sectionKey={sectionKey}
                                sectionData={sections[sectionKey]}
                                houseSystemContext={houseSystemView}
                            />
                        )
                    })}
                </div>
            </DeduplicationProvider>
        </div>
    )
}

export default AstrologyProfile
