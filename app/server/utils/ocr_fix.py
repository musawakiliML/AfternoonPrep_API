import re

# Test the function with your text
text = """Which of the following diagrams correctly illustrates the passage of white light through a triangular glass prism? (A) (B) (C) (D) Yellow Yellow ndigo ! Indigo T Yellow Yellow Indigo Indigo 26. The refractive indices of water and glass with respect to air are 1 and 2/ 4 respectively. If the speed of white light in glass is 2.00 X 108 ms1, , calculate its speed in water. A. 1.33 x 108 ms-1 B. 1.50 x 108 ms-1 C. 2.25 x 108 ms-1 D. 2.67 X 108 ms-1 27. Optical fibres are based on the principle of A. total internal reflection. B. double refraction. C. diffraction. D. interference. 28. When an object is placed 12 cm from a converging lens, a real image four times its original size is produced. Calculate the focal length of the lens. A. 48.0 cm B. 16.0 cm C. 9.6 cm D. 3.0 cm 29. Which of the following statements about sound waves are correct? I. In a uniform medium, the intensity of sound waves is directly proportional to the distance from the source. II. The amplitude of sound waves of given frequency and wave length is a measure of the energy of the waves. III. Pitch is the effect of frequency of sound waves on the human ear. A. I and II only B. II and III only C. I and III only D. I, II and III 3001 8 30. For an astronomical telescope in normal adjustment, the distance between the lenses is A. fo - fe. B. fe + fo. C. foxfe. D. 2fo-fe. - 31. The pitch of a musical note depends on A. amplitude. B. frequency. C. intensity. D. quality. 32. Two sonometer wires, X and Y, have the same length. If the mass per unit length of X is 1 tha that of Y, determine the ratio of the frequency of X to that of Y. A. 2 3 B. 3 2 C. 1:9 D. 3 1 33. The first resonant length of the air column vibrating to a tuning fork in a closed tube is 26.25 cm. Neglecting end correction, calculate the frequency of the fork. [ Speed of sound in air = 336 ms-1 ] A. 960 Hz B. 640 Hz C. 320 Hz D. 160 Hz 34. The derived unit for the universal gravitational constant G is A. Nm-2 kg-2. B. Nm-2 kg. C. Nm2 kg-2. D. Nm kg-2. 35. Static electricity is produced by either loss or gain of A. electrons. B. protons. C. neutrons. D. atoms. 36. An insulated negatively charged rod is held high above the cap of a positively charged electroscope. Tl rod is slowly moved down towards the cap until it is just above it. The leaves of the electroscope will 1 observed to slowly A. collapse completely. B. collapse and then diverge. C. attain maximum divergence. D. diverge and then collapse completely. 3001 9 37. A total charge of 1.0 millicoulomb is stored by the capacitors in the circuit illustrated below. Calculate the value of X. X UF 2UF 100V A. 4.0 uF B. 6.0 uF C. 8.0 uF D. 10.0 uF 38. Electrical energy stored in a capacitor is given by the expression A. 1 CV. 1 2 1 B. CQ2. 2 C. 1 2v. 1 D. 2 C2 39. A 120 l2 resistor is connected across an a.c. having a maximum voltage of 283 V. Calculate the rms value of the current in the circuit. A. 3.3 A B. 2.4 A C. 1.7 A D. 0.6 A 40. 10.54 7.5g G 12n R 20V Use the circuit diagram above to determine the value of R at null deflection. A. 22.2 B. 16 l2 C. 10 l2 D. 9 SQ 3001 10 41. Which of the following methods is the most effective for making a magnet? A. Single touch method B. Divided touch method C. Electrical method D. Hammering in the earth's magnetic field 42. Which of the following factors does not increase the strength of an induced emf in a solenoid? The A. cross-sectional area of the solenoid B. polarity of the magnet facing the solenoid C. speed at which the magnet moves D. number of turns of the solenoid 43. Two identical parallel conductors close to each other carry equal currents in the same direction. Which of the following statements is not correct? A. Each of the conductors will experience a force B. Each of the conductors can move C. The magnitudes of the forces on the conductors will be equal D. The two conductors will repel each other 44. In the wiring of houses, the switch is connected to the A. earth wire. B. live wire. C. neutral wire. D. earth and neutral wires bridged together. 45. A circuit consisting of a resistor R, an inductor L and a capacitor C in series is connected to an alternating current source. At resonance, the A. current is maximum. B. impedance is maximum. C. current is least. D. frequency is maximum. 46. Which of the following radiations is not part of the electromagnetic spectrum? A. Gamma ray B. Alpha particle C. X-ray D. Radio wave 47. Which of the following constituents of an atom enables matter to conduct electricity? A. Electrons B. Neutrons C. Protons D. Nucleus 3001 11 0.0eV IV - 0.85eV 48. - 1.50eV II - 3.4eV I Ground state The diagram above illustrates some energy levels in an atom of hydrogen. Which of the transitions I - IV will produce an absorption spectra line in the hydrogen emission spectrum? A. IV B. III C. II D. I 49. Radium (Ra) disintegrates as illustrated in the equation below. Identify particles X and Y. 222 Ra 217 86 Rn + 4X + !Y 88 A. Alpha and beta B. Beta and Alpha C. Alpha and neutron D. Neutron and beta 50. It is not very possible to determine, exactly and simultaneously, both the position and momentum of a particle. This statement is called the
"""

# Define a regex pattern to match question numbers and text
pattern = r'(\d\d+\..+?)(?=(?:\d+\.\s+\.|$)|$)'

# Use re.split to split the text into individual questions
question_texts = re.split(pattern, text)[1:]

# Combine the question numbers and texts with answer choices
questions = []
for i in range(0, len(question_texts), 2):
    question_number_text = question_texts[i]
    if i + 1 < len(question_texts):
        answer_choices_text = question_texts[i + 1]
    else:
        answer_choices_text = ""

    # Split answer choices into a list
    answer_choices = re.findall(r'[A-D]\..+?(?=[A-D]\.|$)', answer_choices_text)

    # Append the question and answer choices to the list
    questions.append((question_number_text.strip(), answer_choices))

# Print the extracted questions and answer choices
for q, choices in questions:
    print("Question:", q)
    print("Answer Choices:", choices)
    print()
