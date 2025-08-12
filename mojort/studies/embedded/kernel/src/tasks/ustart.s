.section .text

.global task1_entry
task1_entry:
    bl user_main1
    b .

.global task2_entry
task2_entry:
    bl user_main2
    b .
