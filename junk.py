from abstract_format import SpacyAbstractFormatter

abstract =""" The multi-leaf collimator (MLC)-equipped CyberKnife(®) M6 radiosurgery system (CKM6) (Accuray Inc., Sunnyvale, CA) has been increasingly employed for stereotactic radiosurgery (SRS) to treat relatively small lesions. However, achieving an accurate dose distribution in such cases is usually challenging due to the combination of numerous small fields ≤ (30 × 30) mm(2) . In this study, we developed a new Monte Carlo (MC) dose model for the CKM6 system using the EGSnrc to investigate dose variations in the small fields. The dose model was verified for the static MLC fields ranging from (53.8 × 53.9) to (7.6 × 7.7) mm(2) at 800 mm source to axis distance in a water phantom, based on the computed doses of Accuray Precision(®) (Accuray Inc.) treatment planning system (TPS). We achieved a statistical uncertainty of ≤4% by simulating 30-50 million incident particles/histories. Then, the treatment plans were created for the same fields in the TPS, and the corresponding measurements were performed with MapCHECK2 (Sun Nuclear Corporation), a standard device for patient-specific quality assurance (PSQA). Results of the MC simulations, TPS, and MapCHECK2 measurements were inter-compared. An overall difference in dosimetric parameters such as profiles, tissue maximum ratio (TMR), and output factors (OF) between the MC simulations and the TPS results was found ≤3% for (53.8 × 53.9-15.4 × 15.4) mm(2) MLC fields, and it rose to 4.5% for the smallest (7.6 mm × 7.7 mm) MLC field. The MapCHECK2 results showed a deviation ranging from -1.5% to + 4.5% compared to the TPS results, whereas the deviation was within ±2.5% compared with the MC results. Overall, our MC dose model for the CKM6 system showed better agreement with measurements and it could serve as a secondary dose verification tool for the patient-specific QA in small fields.
"""

formatter = SpacyAbstractFormatter(line_width=100)
result = formatter.format_abstract(abstract)

print(f"Original: {abstract}")
print("f\n\n\n")

print(result)