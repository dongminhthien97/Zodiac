import { useDeduplication } from './DeduplicationProvider'
import { LAYERS, LayerConfig } from '../../constants/layers.ts'

interface BulletCardProps {
    text: string;
    layerId: string;
}

const BulletCard = ({ text, layerId }: BulletCardProps) => {
    const { trackContent, isRendered } = useDeduplication()

    // First check if already rendered
    if (isRendered(text)) {
        return null
    }

    // Attempt to track
    const isNew = trackContent(text)
    if (!isNew) {
        return null
    }

    const layerConfig: LayerConfig | undefined = LAYERS[layerId as keyof typeof LAYERS]
    const Icon = layerConfig?.icon

    return (
        <article className={`bullet-card layer-${layerId}`}>
            <div className="bullet-content">
                {Icon && (
                    <div className="bullet-icon">
                        <Icon size={18} />
                    </div>
                )}
                <div className="bullet-text">
                    {text}
                </div>
            </div>

            <style>{`
                .bullet-card {
                    padding: 16px;
                    border-radius: var(--radius-md);
                    margin-bottom: 12px;
                    background: var(--white-05);
                    border: 1px solid var(--white-10);
                    transition: all 0.2s ease;
                }
                .bullet-card:hover {
                    background: var(--white-10);
                    transform: translateX(4px);
                }
                .bullet-content {
                    display: flex;
                    gap: 12px;
                }
                .bullet-icon {
                    flex-shrink: 0;
                    margin-top: 2px;
                }
                .bullet-text {
                    font-size: 15px;
                    line-height: 1.6;
                    color: var(--white-70);
                    max-width: 68ch;
                }
                .layer-psychological .bullet-icon { color: var(--gold-primary); }
                .layer-spiritual .bullet-icon { color: var(--nebula-purple); }
                .layer-practical .bullet-icon { color: #10b981; } /* Mint color */
                
                .layer-psychological { border-left: 3px solid var(--gold-primary); }
                .layer-spiritual { border-left: 3px solid var(--nebula-purple); }
                .layer-practical { border-left: 3px solid #10b981; }
            `}</style>
        </article>
    )
}

export default BulletCard
