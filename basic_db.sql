
-- Обновление бюджета для пользователя (замените 'user_id' на ваш конкретный идентификатор пользователя)
UPDATE api_userprofile
SET budget_limit = 500
WHERE user_id = '660339bdcb081f7aafe98d5d';

-- Добавление категорий
INSERT INTO api_category (name) VALUES 
('Groceries'),
('Digital'),
('Others');

-- Получение id для категорий
DO $$
DECLARE
    groceries_id INTEGER;
    digital_id INTEGER;
    others_id INTEGER;
BEGIN
    SELECT id INTO groceries_id FROM api_category WHERE name = 'Groceries';
    SELECT id INTO digital_id FROM api_category WHERE name = 'Digital';
    SELECT id INTO others_id FROM api_category WHERE name = 'Others';

    -- Добавление транзакций
    INSERT INTO api_transaction  (name, date, amount, type, category_id, from_account, note, owner_id) VALUES
    ('McDonalds', CURRENT_DATE, 25, 'Expense', groceries_id, 'Savings', 'Groceries', '660339bdcb081f7aafe98d5d'),
    ('Internet', CURRENT_DATE, 25, 'Expense', digital_id, 'Savings', 'Internet', '660339bdcb081f7aafe98d5d'),
    ('Shops', CURRENT_DATE, 25, 'Expense', others_id, 'Savings', 'Shops', '660339bdcb081f7aafe98d5d'),
    ('Salary', CURRENT_DATE, 25, 'Income', digital_id, 'Savings', 'Salary', '660339bdcb081f7aafe98d5d'),
    ('Freelance', CURRENT_DATE, 25, 'Income', digital_id, 'Savings', 'Freelance', '660339bdcb081f7aafe98d5d');
END $$;
