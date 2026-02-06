import React from 'react'
import { useDeduplication } from './DeduplicationProvider'
import { LAYERS } from '../../constants/layers'
import clsx from 'clsx'

const BulletCard = ({ text, layerId }) => {
    const { trackContent, isRendered } = useDeduplication()

    // First check if already rendered
    if (isRendered(text)) {
        return null
    }

    // Attempt to track. If it returns false, it means it was just added by another component 
    // in this same pass (highly unlikely in sequential React render, but good safety)
    // or logic inside trackContent determined it's a dupe.
    // Actually, trackContent modifies the ref, so we call it here.
    const isNew = trackContent(text)
    if (!isNew) {
        return null
    }

    const layerConfig = LAYERS[layerId]
    const Icon = layerConfig?.icon

    return (
        <article
            className={clsx(
                "rounded-lg p-3 sm:p-4 mb-3 last:mb-0 transition-all duration-200",
                "border border-white/5 bg-white/5 hover:bg-white/10",
                "text-white/90 shadow-sm",

                // Dynamic layer styling
                layerId === 'psychological' && "psychological-card",
                layerId === 'spiritual' && "spiritual-card",
                layerId === 'practical' && "practical-card"
            )}
        >
            <div className="flex gap-3">
                {Icon && (
                    <div className={clsx(
                        "mt-1 shrink-0",
                        layerId === 'psychological' && "text-gold-400",
                        layerId === 'spiritual' && "text-nebula-400",
                        layerId === 'practical' && "text-mint-400"
                    )}>
                        <Icon size={18} />
                    </div>
                )}
                <div className="content-text leading-relaxed text-sm sm:text-base max-w-[68ch]">
                    {text}
                </div>
            </div>
        </article>
    )
}

export default BulletCard
