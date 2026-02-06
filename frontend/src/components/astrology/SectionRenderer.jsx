import React from 'react'
import LayerBlock from './LayerBlock'
import { SECTION_LABELS } from '../../constants/sections'
import { useUserPreferences, useExpansionState } from '../../contexts/UserPreferencesContext'

const SectionRenderer = ({ sectionKey, sectionData, houseSystemContext }) => {
    const { language, detailLevel } = useUserPreferences()

    if (!sectionData) return null

    // Helper to determine if a layer should be expanded by default
    const getDefaultExpanded = (layerId) => {
        if (detailLevel === 'full') return true
        // In overview mode, only 'psychological' is expanded by default
        return layerId === 'psychological'
    }

    const layers = ['psychological', 'spiritual', 'practical']
    const label = SECTION_LABELS[sectionKey] ? SECTION_LABELS[sectionKey][language] : sectionKey

    return (
        <div className="mb-12 last:mb-0 scroll-mt-20" id={`section-${sectionKey}`}>
            <h2 className="mb-6 font-display text-2xl font-bold text-white relative pl-4 border-l-4 border-white/20">
                {label}
            </h2>

            <div className="space-y-4">
                {layers.map(layerId => {
                    // Unique ID for state persistence: "houseSystem-sectionKey-layerId"
                    const stateId = `${sectionKey}-${layerId}`

                    // Use our custom hook which handles the storage logic
                    const [isExpanded, toggle] = useExpansionState(
                        houseSystemContext, // Scope to current house system
                        stateId,
                        getDefaultExpanded(layerId)
                    )

                    return (
                        <LayerBlock
                            key={layerId}
                            layerId={layerId}
                            bullets={sectionData[layerId]}
                            language={language}
                            isExpanded={isExpanded}
                            onToggle={() => toggle(!isExpanded)}
                        />
                    )
                })}
            </div>
        </div>
    )
}

export default SectionRenderer
