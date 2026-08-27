/**
 * ==========================================================================
 * FINANCIAL CALCULATOR ENGINE (CALCULATORS.JS)
 * Stock Averaging, Compound Interest, Dividend Yield Simulators
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initStockAverageCalc();
  initCompoundInterestCalc();
});

/* ==========================================================================
   1. 주식 물타기 / 추가매수 평단가 계산기
   ========================================================================== */
function initStockAverageCalc() {
  const form = document.getElementById('stockAvgForm');
  if (!form) return;

  const currentPriceInput = document.getElementById('calcCurPrice');
  const currentQtyInput = document.getElementById('calcCurQty');
  const addPriceInput = document.getElementById('calcAddPrice');
  const addQtyInput = document.getElementById('calcAddQty');
  const targetPriceInput = document.getElementById('calcTargetPrice');

  function calculate() {
    const curPrice = parseFloat(currentPriceInput?.value) || 0;
    const curQty = parseFloat(currentQtyInput?.value) || 0;
    const addPrice = parseFloat(addPriceInput?.value) || 0;
    const addQty = parseFloat(addQtyInput?.value) || 0;
    const targetPrice = parseFloat(targetPriceInput?.value) || 0;

    const initialTotal = curPrice * curQty;
    const addedTotal = addPrice * addQty;
    const totalQty = curQty + addQty;
    const finalTotal = initialTotal + addedTotal;

    if (totalQty === 0) return;

    const newAvgPrice = Math.round(finalTotal / totalQty);
    const dropRate = curPrice > 0 ? (((newAvgPrice - curPrice) / curPrice) * 100).toFixed(2) : 0;

    // Display Results
    const resAvgPrice = document.getElementById('resAvgPrice');
    const resTotalQty = document.getElementById('resTotalQty');
    const resTotalInvest = document.getElementById('resTotalInvest');
    const resDropRate = document.getElementById('resDropRate');
    const resTargetReturn = document.getElementById('resTargetReturn');

    if (resAvgPrice) resAvgPrice.textContent = newAvgPrice.toLocaleString() + '원';
    if (resTotalQty) resTotalQty.textContent = totalQty.toLocaleString() + '주';
    if (resTotalInvest) resTotalInvest.textContent = Math.round(finalTotal).toLocaleString() + '원';
    
    if (resDropRate) {
      const isDown = parseFloat(dropRate) < 0;
      resDropRate.textContent = `${dropRate}% ${isDown ? '하락 (평단 절감)' : '상승'}`;
      resDropRate.style.color = isDown ? 'var(--accent-emerald)' : 'var(--accent-red)';
    }

    if (resTargetReturn && targetPrice > 0) {
      const returnRate = (((targetPrice - newAvgPrice) / newAvgPrice) * 100).toFixed(2);
      const profitVal = Math.round((targetPrice - newAvgPrice) * totalQty);
      resTargetReturn.textContent = `${returnRate}% (${profitVal.toLocaleString()}원)`;
      resTargetReturn.style.color = parseFloat(returnRate) >= 0 ? 'var(--accent-red)' : 'var(--accent-blue)';
    }

    // Update Visual Comparison Bar
    const barInitial = document.getElementById('progressInitial');
    const barAdded = document.getElementById('progressAdded');
    if (barInitial && barAdded && finalTotal > 0) {
      const initPercent = (initialTotal / finalTotal) * 100;
      const addedPercent = (addedTotal / finalTotal) * 100;
      barInitial.style.width = initPercent + '%';
      barAdded.style.width = addedPercent + '%';
    }
  }

  [currentPriceInput, currentQtyInput, addPriceInput, addQtyInput, targetPriceInput].forEach(input => {
    input?.addEventListener('input', calculate);
  });

  document.getElementById('btnResetAvg')?.addEventListener('click', () => {
    form.reset();
    calculate();
  });

  // Initial calculation trigger
  calculate();
}

/* ==========================================================================
   2. 복리 수익률 & 적립식 투자 계산기
   ========================================================================== */
function initCompoundInterestCalc() {
  const form = document.getElementById('compoundForm');
  if (!form) return;

  const initialPrincipalInput = document.getElementById('calcPrincipal');
  const monthlyDepositInput = document.getElementById('calcMonthly');
  const annualRateInput = document.getElementById('calcRate');
  const yearsInput = document.getElementById('calcYears');

  function calculateCompound() {
    const principal = parseFloat(initialPrincipalInput?.value) || 0;
    const monthly = parseFloat(monthlyDepositInput?.value) || 0;
    const annualRate = (parseFloat(annualRateInput?.value) || 0) / 100;
    const years = parseFloat(yearsInput?.value) || 1;

    const months = years * 12;
    const monthlyRate = annualRate / 12;

    let totalAmount = principal;
    let totalPrincipal = principal;

    for (let m = 1; m <= months; m++) {
      totalAmount = totalAmount * (1 + monthlyRate) + monthly;
      totalPrincipal += monthly;
    }

    const totalInterest = totalAmount - totalPrincipal;
    const profitRate = totalPrincipal > 0 ? ((totalInterest / totalPrincipal) * 100).toFixed(1) : 0;

    const resTotal = document.getElementById('resCompoundTotal');
    const resPrincipal = document.getElementById('resCompoundPrincipal');
    const resInterest = document.getElementById('resCompoundInterest');
    const resRate = document.getElementById('resCompoundRate');

    if (resTotal) resTotal.textContent = Math.round(totalAmount).toLocaleString() + '원';
    if (resPrincipal) resPrincipal.textContent = Math.round(totalPrincipal).toLocaleString() + '원';
    if (resInterest) resInterest.textContent = Math.round(totalInterest).toLocaleString() + '원';
    if (resRate) resRate.textContent = `+${profitRate}%`;
  }

  [initialPrincipalInput, monthlyDepositInput, annualRateInput, yearsInput].forEach(input => {
    input?.addEventListener('input', calculateCompound);
  });

  calculateCompound();
}
