# Lesson 01 Mojo exercises (to implement on the M2)

1. Run the official vector addition example unchanged.
2. Verify GPU device selection and full input/output correctness.
3. Create `normalize.mojo`: `uint8` image → float normalized to `[0,1]`.
4. Compare 64×64, 256×256, and 720×1280 inputs.
5. Test on odd widths that don't divide your chosen block size.
6. Document GPU synchronization and memory transfer timing separately.

Do not mark the lesson complete until GPU code actually runs on the laptop.
