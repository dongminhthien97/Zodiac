import { clsx } from 'clsx'
import { HOUSE_SYSTEMS } from '../../constants/layers.ts'
import { useUserPreferences } from '../../contexts/UserPreferencesContext'

interface HouseSystemToggleProps {
    availableSystems: string;
    currentSystem: 'whole_sign' | 'placidus';
    onSwitch: (newSystem: 'whole_sign' | 'placidus') => void;
}

const HouseSystemToggle = ({ availableSystems, currentSystem, onSwitch }: HouseSystemToggleProps) => {
    const { language } = useUserPreferences()

    // If only one system is available ('whole_sign' or 'placidus' in meta),
    // we effectively show a static indicator or disabled toggle?
    // Requirements say: "Disable Placidus toggle visually" etc.

    const isWholeSignDisabled = availableSystems === 'placidus'
    const isPlacidusDisabled = availableSystems === 'whole_sign'

    return (
        <div className="flex justify-center mb-8">
            <div className="bg-white/10 p-1 rounded-xl inline-flex relative shadow-inner">
                {/* Sliding background for active state - mostly for visual flair */}
                <div
                    className={clsx(
                        "absolute top-1 bottom-1 w-[calc(50%-4px)] bg-ink-700 rounded-lg shadow-sm transition-all duration-300 ease-out",
                        currentSystem === 'whole_sign' ? "left-1" : "left-[calc(50%+2px)]"
                    )}
                />

                <button
                    onClick={() => !isWholeSignDisabled && onSwitch('whole_sign')}
                    disabled={isWholeSignDisabled}
                    className={clsx(
                        "relative px-6 py-2 rounded-lg text-sm font-medium transition-colors z-10 w-32",
                        currentSystem === 'whole_sign'
                            ? "text-white"
                            : "text-white/60 hover:text-white/90",
                        isWholeSignDisabled && "opacity-30 cursor-not-allowed hover:text-white/60"
                    )}
                >
                    {HOUSE_SYSTEMS.whole_sign[language as 'vi' | 'en']}
                </button>

                <button
                    onClick={() => !isPlacidusDisabled && onSwitch('placidus')}
                    disabled={isPlacidusDisabled}
                    className={clsx(
                        "relative px-6 py-2 rounded-lg text-sm font-medium transition-colors z-10 w-32",
                        currentSystem === 'placidus'
                            ? "text-white"
                            : "text-white/60 hover:text-white/90",
                        isPlacidusDisabled && "opacity-30 cursor-not-allowed hover:text-white/60"
                    )}
                >
                    {HOUSE_SYSTEMS.placidus[language as 'vi' | 'en']}
                </button>
            </div>
        </div>
    )
}

export default HouseSystemToggle
