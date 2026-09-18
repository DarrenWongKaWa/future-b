program nk_eval_driver
  use, intrinsic :: iso_fortran_env, only: real64, int64
  use native_kernel_runtime_v1
  use generated_da_kernel
  implicit none
  logical :: accepted, ell_R_valid, exact_y_evaluated
  integer(int64) :: reject_stage, status, accepted_i, ell_R_valid_i, exact_y_i
  real(real64) :: ell_hat, ell_R
  real(real64) :: log_q_reverse_minus_forward, u1, u2
  integer(int64) :: exact_x_valid_i
  logical :: exact_x_valid
  real(real64) :: exact_log_weight_x
  real(real64) :: x_k
  real(real64) :: x_q(1)
  real(real64) :: x_tau(2)
  real(real64) :: x_t
  real(real64) :: x_omega
  real(real64) :: x_g
  integer(int64) :: x_L
  real(real64) :: x_delta
  real(real64) :: x_gap
  real(real64) :: y_k
  real(real64) :: y_q(1)
  real(real64) :: y_tau(2)
  real(real64) :: y_t
  real(real64) :: y_omega
  real(real64) :: y_g
  integer(int64) :: y_L
  real(real64) :: y_delta
  real(real64) :: y_gap
  read(*,*) x_k
  read(*,*) x_q
  read(*,*) x_tau
  read(*,*) x_t
  read(*,*) x_omega
  read(*,*) x_g
  read(*,*) x_L
  read(*,*) x_delta
  read(*,*) x_gap
  read(*,*) y_k
  read(*,*) y_q
  read(*,*) y_tau
  read(*,*) y_t
  read(*,*) y_omega
  read(*,*) y_g
  read(*,*) y_L
  read(*,*) y_delta
  read(*,*) y_gap
  read(*,*) log_q_reverse_minus_forward, u1, u2
  read(*,*) exact_x_valid_i, exact_log_weight_x
  exact_x_valid = (exact_x_valid_i /= 0_int64)
  call evaluate_da_kernel(&
    x_k, x_q, x_tau, x_t, x_omega, x_g, x_L, x_delta, x_gap, y_k, y_q, y_tau, y_t, &
      y_omega, y_g, y_L, y_delta, y_gap, log_q_reverse_minus_forward, u1, u2, &
      exact_x_valid, exact_log_weight_x, accepted, reject_stage, ell_hat, ell_R_valid, &
      ell_R, exact_y_evaluated, status)
  accepted_i = merge(1_int64, 0_int64, accepted)
  ell_R_valid_i = merge(1_int64, 0_int64, ell_R_valid)
  exact_y_i = merge(1_int64, 0_int64, exact_y_evaluated)
  write(*,'(I0,1X,I0,1X,I0,1X,ES24.16E3,1X,I0,1X,ES24.16E3,1X,I0,1X,I0,1X,I0,1X,I0,1X,I0,1X,I0)') &
    status, accepted_i, reject_stage, ell_hat, ell_R_valid_i, ell_R, exact_y_i, &
    nk_n_electron_twoband, nk_n_vertex_sigmaz, nk_n_matmul, nk_n_trace, nk_n_exact_graph
end program nk_eval_driver
