/**
 * Quality Validation Runner for Astrology Content Engine v1.0.0
 * Validates generated content against all production requirements
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load sample data
const samplePath = path.join(__dirname, '../data/libra_sample_v1.json');
const sampleData = JSON.parse(fs.readFileSync(samplePath, 'utf8'));

class QualityValidator {
    constructor() {
        this.errors = [];
        this.warnings = [];
        this.stats = {
            totalSentences: 0,
            sentenceLengths: [],
            duplicates: 0
        };
    }

    // Validation 1: Zero sentence duplication
    validateNoDuplicates() {
        const seen = new Set();
        let duplicateCount = 0;

        for (const section of sampleData.sections) {
            for (const item of section.items) {
                for (const sentence of item.sentences) {
                    const normalized = sentence.trim().toLowerCase();
                    if (seen.has(normalized)) {
                        duplicateCount++;
                        this.errors.push(`Duplicate sentence: "${sentence.substring(0, 50)}..."`);
                    }
                    seen.add(normalized);
                    this.stats.totalSentences++;
                }
            }
        }

        this.stats.duplicates = duplicateCount;
        return duplicateCount === 0;
    }

    // Validation 2: Sentence length 18-30 words
    validateSentenceLength() {
        let violations = 0;

        for (const section of sampleData.sections) {
            for (const item of section.items) {
                for (const sentence of item.sentences) {
                    const words = sentence.trim().split(/\s+/);
                    const wordCount = words.length;

                    this.stats.sentenceLengths.push(wordCount);

                    if (wordCount < 18 || wordCount > 30) {
                        violations++;
                        this.warnings.push(
                            `${item.id}: Sentence ${wordCount} words (expected 18-30): "${sentence.substring(0, 40)}..."`
                        );
                    }
                }
            }
        }

        return violations === 0;
    }

    // Validation 3: Schema compliance
    validateSchema() {
        const requiredMeta = ['version', 'content_hash', 'locale', 'generated_at'];
        const requiredContext = ['zodiac', 'element', 'birth_time_known', 'interpretation_mode'];
        const expectedSections = ['big_picture', 'core_identity', 'love_drive', 'collective', 'soul_lessons', 'conclusion'];

        // Check meta
        for (const field of requiredMeta) {
            if (!sampleData.meta[field]) {
                this.errors.push(`Missing meta.${field}`);
            }
        }

        // Check context
        for (const field of requiredContext) {
            if (sampleData.context[field] === undefined) {
                this.errors.push(`Missing context.${field}`);
            }
        }

        // Check section order
        const actualSections = sampleData.sections.map(s => s.key);
        if (JSON.stringify(actualSections) !== JSON.stringify(expectedSections)) {
            this.errors.push(`Section order mismatch. Expected: ${expectedSections.join(', ')}, Got: ${actualSections.join(', ')}`);
        }

        // Check items structure
        for (const section of sampleData.sections) {
            for (const item of section.items) {
                if (!item.id) this.errors.push(`Section ${section.key}: missing item.id`);
                if (!item.layer) this.errors.push(`Section ${section.key}: missing item.layer`);
                if (!item.sentences || !Array.isArray(item.sentences)) {
                    this.errors.push(`Section ${section.key}: invalid item.sentences`);
                }
            }
        }

        return this.errors.length === 0;
    }

    // Validation 4: House logic correctness
    validateHouseLogic() {
        const { birth_time_known, house_system } = sampleData.context;

        if (!birth_time_known) {
            // Should have no house system
            if (house_system !== null) {
                this.errors.push(`House system specified (${house_system}) without birth time`);
            }

            // Should have no house numbers in items
            for (const section of sampleData.sections) {
                for (const item of section.items) {
                    if (item.house !== undefined && item.house !== null) {
                        this.errors.push(`House number found in ${item.id} without birth time`);
                    }
                }
            }
        }

        return this.errors.length === 0;
    }

    // Run all validations
    runAll() {
        console.log('🔍 Running Quality Validation Suite...\n');

        const result = {
            duplication: this.validateNoDuplicates(),
            sentenceLength: this.validateSentenceLength(),
            schema: this.validateSchema(),
            houseLogic: this.validateHouseLogic()
        };

        console.log('📊 Validation Results:\n');
        console.log(`✅ Zero Duplication: ${result.duplication ? 'PASS' : 'FAIL'}`);
        console.log(`✅ Sentence Length: ${result.sentenceLength ? 'PASS' : 'FAIL'}`);
        console.log(`✅ Schema Compliance: ${result.schema ? 'PASS' : 'FAIL'}`);
        console.log(`✅ House Logic: ${result.houseLogic ? 'PASS' : 'FAIL'}`);

        console.log('\n📈 Statistics:');
        console.log(`Total Sentences: ${this.stats.totalSentences}`);
        console.log(`Duplicates Found: ${this.stats.duplicates}`);

        if (this.stats.sentenceLengths.length > 0) {
            const avg = this.stats.sentenceLengths.reduce((a, b) => a + b, 0) / this.stats.sentenceLengths.length;
            const min = Math.min(...this.stats.sentenceLengths);
            const max = Math.max(...this.stats.sentenceLengths);
            console.log(`Sentence Length: min=${min}, max=${max}, avg=${avg.toFixed(1)}`);
        }

        if (this.errors.length > 0) {
            console.log('\n❌ Errors:');
            this.errors.forEach(e => console.log(`  - ${e}`));
        }

        if (this.warnings.length > 0) {
            console.log('\n⚠️  Warnings:');
            this.warnings.slice(0, 5).forEach(w => console.log(`  - ${w}`));
            if (this.warnings.length > 5) {
                console.log(`  ... and ${this.warnings.length - 5} more`);
            }
        }

        const allPassed = Object.values(result).every(v => v === true) && this.errors.length === 0;

        console.log(`\n${allPassed ? '✅ ALL VALIDATIONS PASSED' : '❌ VALIDATION FAILED'}\n`);

        return allPassed;
    }
}

// Run validation
const validator = new QualityValidator();
const passed = validator.runAll();

process.exit(passed ? 0 : 1);
