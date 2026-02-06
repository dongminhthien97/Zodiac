import React from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import clsx from 'clsx'
import BulletCard from './BulletCard'
import { LAYERS } from '../../constants/layers'

const LayerBlock = ({ layerId, bullets, isExpanded, onToggle, language = 'vi' }) => {
    if (!bullets || bullets.length === 0) return null

    const layerConfig = LAYERS[layerId]
    if (!layerConfig) return null

    const title = layerConfig.label[language]
    const description = layerConfig.description[language]

    return (
        <section className="mb-4 last:mb-0">
            <button
                onClick={onToggle}
                className={clsx(
                    "flex w-full items-center justify-between rounded-lg p-3 text-left transition-colors",
                    "hover:bg-white/5 focus:outline-none focus:ring-2 focus:ring-white/20",
                    isExpanded ? "bg-white/5" : "bg-transparent"
                )}
                aria-expanded={isExpanded}
            >
                <div className="flex items-center gap-3">
                    {/* Visual indicator line */}
                    <div className={clsx(
                        "h-6 w-1 rounded-full",
                        layerId === 'psychological' && "bg-gold-500",
                        layerId === 'spiritual' && "bg-nebula-500",
                        layerId === 'practical' && "bg-mint-500"
                    )} />

                    <div>
                        <h3 className={clsx(
                            "font-display font-medium",
                            layerId === 'psychological' && "text-gold-100",
                            layerId === 'spiritual' && "text-nebula-100",
                            layerId === 'practical' && "text-mint-100"
                        )}>
                            {title}
                        </h3>
                        {/* Show valid bullet count preview if collapsed? Optional, keeping simple for now */}
                    </div>
                </div>

                <div className="text-white/50">
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </div>
            </button>

            {isExpanded && (
                <div className="mt-2 pl-2 sm:pl-4 space-y-2 animate-in fade-in slide-in-from-top-1 duration-200">
                    {/* Mobile-only accessible description if needed, or tooltip */}
                    {/* <p className="text-xs text-white/40 mb-3 italic">{description}</p> */}

                    <div className="space-y-3 pt-2">
                        {bullets.map((text, idx) => (
                            // Use index and text slice for key to be reasonably unique but stable before hashing checks
                            <BulletCard
                                key={`${idx}-${text.substring(0, 10)}`}
                                text={text}
                                layerId={layerId}
                            />
                        ))}
                    </div>
                </div>
            )}
        </section>
    )
}

export default LayerBlock
