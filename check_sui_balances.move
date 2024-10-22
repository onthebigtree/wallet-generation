module my_address::balance_checker {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    public entry fun check_balance(address: address, ctx: &mut TxContext) {
        let balance = coin::balance<SUI>(address);
        // 在实际应用中，你可能想要将余额返回或者触发某个事件
        // 这里我们只是将余额打印到控制台
        std::debug::print(&balance);
    }

    // 一个辅助函数，用于将一些 SUI 代币发送到指定地址
    public entry fun send_sui(amount: u64, recipient: address, ctx: &mut TxContext) {
        let coin = coin::mint_for_testing<SUI>(amount, ctx);
        transfer::transfer(coin, recipient);
    }
}