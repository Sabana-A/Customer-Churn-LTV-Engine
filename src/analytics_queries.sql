-- 1. Total customers
SELECT COUNT(*) AS total_customers
FROM telco_customer_churn;

-- 2. Churned customers
SELECT COUNT(*) AS churned_customers
FROM telco_customer_churn
WHERE "Churn" = 'Yes';

-- 3. Churn by contract
SELECT
    "Contract",
    COUNT(*) AS customers,
    SUM(CASE WHEN "Churn" = 'Yes' THEN 1 ELSE 0 END) AS churned_customers
FROM telco_customer_churn
GROUP BY "Contract";