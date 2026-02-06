import { Zap, Moon, Compass, LucideIcon } from 'lucide-react'

// Layer configuration for the astrology engine

export interface LayerConfig {
    order: number;
    id: string;
    label: { vi: string; en: string };
    style: string;
    icon: LucideIcon;
    description: { vi: string; en: string };
}

export const LAYERS: Record<string, LayerConfig> = {
    psychological: {
        order: 1,
        id: 'psychological',
        label: { vi: 'Tâm lý', en: 'Psychological' },
        style: 'layer-primary',
        icon: Zap,
        description: { vi: 'Phân tích chiều sâu tâm lý và tính cách', en: 'Deep psychological and personality analysis' }
    },
    spiritual: {
        order: 2,
        id: 'spiritual',
        label: { vi: 'Tâm linh', en: 'Spiritual' },
        style: 'layer-secondary',
        icon: Moon,
        description: { vi: 'Bài học linh hồn và nghiệp quả', en: 'Soul lessons and karmic patterns' }
    },
    practical: {
        order: 3,
        id: 'practical',
        label: { vi: 'Thực hành', en: 'Practical' },
        style: 'layer-accent',
        icon: Compass,
        description: { vi: 'Lời khuyên hành động cụ thể', en: 'Actionable advice and practical steps' }
    }
}

export const HOUSE_SYSTEMS = {
    whole_sign: { vi: 'Whole Sign', en: 'Whole Sign' },
    placidus: { vi: 'Placidus', en: 'Placidus' }
}
