import os
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.utils.audio import AudioProcessor
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.glow_tts import GlowTTS
from trainer import Trainer, TrainerArgs
from TTS.TTS.tts.configs.glow_tts_config import GlowTTSConfig

# Define output path
output_path = "../../tts_train_dir"

# Define dataset configuration
dataset_config = BaseDatasetConfig(
    formatter="ljspeech",
    meta_file_train="metadata.csv",
    path=os.path.join(output_path, "data/")
)

# Initialize audio processor
config = GlowTTSConfig(
    batch_size=32,
    eval_batch_size=16,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=100,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    print_step=25,
    print_eval=False,
    mixed_precision=True,
    output_path=output_path,
    datasets=[dataset_config],
    save_step=1000,
)

try:
    # Initialize audio processor
    ap = AudioProcessor.init_from_config(config)

    # Initialize tokenizer
    tokenizer, config = TTSTokenizer.init_from_config(config)

    # Load dataset samples
    eval_split_size = 1  # Example: set evaluation split size to 10% of the dataset

    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=None,  # Adjust if necessary
        eval_split_size=eval_split_size,
    )

    # Initialize model
    model = GlowTTS(config, ap, tokenizer, speaker_manager=None)

    # Initialize trainer
    trainer = Trainer(
        TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples
    )

    # Start training
    trainer.fit()

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Handle the error as needed
