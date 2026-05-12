; ModuleID = 'test_single_register_variations_truthy'
source_filename = "test_single_register_variations"

define void @test_single_register_variations() #0 {
entry:
  call void @__quantum__rt__initialize(ptr null)
  call void @__quantum__qis__mz__body(ptr null, ptr null)
  %0 = call i1 @__quantum__qis__read_result__body(ptr null)
  br i1 %0, label %then, label %else

then:                                             ; preds = %entry
  %1 = call i1 @__quantum__qis__read_result__body(ptr inttoptr (i64 1 to ptr))
  br i1 %1, label %then1, label %else2

else:                                             ; preds = %entry
  br label %continue

continue:                                         ; preds = %continue3, %else
  ret void

then1:                                            ; preds = %then
  br label %continue3

else2:                                            ; preds = %then
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 1 to ptr))
  br label %continue3

continue3:                                        ; preds = %else2, %then1
  br label %continue
}

declare void @__quantum__rt__initialize(ptr)

declare void @__quantum__qis__mz__body(ptr, ptr writeonly) #1

declare i1 @__quantum__qis__read_result__body(ptr)

attributes #0 = { "entry_point" "output_labeling_schema" "qir_profiles"="custom" "required_num_qubits"="2" "required_num_results"="2" }
attributes #1 = { "irreversible" }

!llvm.module.flags = !{!0, !1, !2, !3}

!0 = !{i32 1, !"qir_major_version", i32 1}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
