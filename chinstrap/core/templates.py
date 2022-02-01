contracts = {
    "Syntax Examples": [
        {
            "fileName": "minimal.py",
            "name": "Minimal",
            "description": "An almost minimal template to start with.",
        },
        {
            "fileName": "welcome.py",
            "name": "Welcome",
            "description": "A small example with a very simple storage and only one small entry point.",
        },
    ],
    "Templates per Type": [
        {
            "fileName": "timelock.py",
            "name": "Timelock",
            "description": "https://tezos.gitlab.io/alpha/timelock.html",
        },
        {
            "fileName": "constants.py",
            "name": "Using Constants",
            "description": "Global table of constants. More at: https://tezos.gitlab.io/protocols/011_hangzhou.html?highlight=global%20table%20constants#global-constants",
        },
        {
            "fileName": "onchain_views.py",
            "name": "Using on-chain views",
            "description": "The documentation can be found https://smartpy.io/docs/experimental/onchain_views/",
        },
        {
            "fileName": "upgradable_lambdas.py",
            "name": "Upgradable Contract",
            "description": "An entry point that accepts packed values and calls an upgradable lambda.",
        },
        {
            "fileName": "create_contract.py",
            "name": "Contract creation",
            "description": 'Using <span class="code">sp.create_contract</span>.',
        },
        {
            "fileName": "bls12_381.py",
            "name": "BLS12 381",
            "description": 'Various BLS12 operations using types <span class="code">sp.TBls12_381_g1</span>, <span class="code">sp.TBls12_381_g2</span>, <span class="code">sp.TBls12_381_fr</span>.',
        },
        {
            "fileName": "collatz.py",
            "name": "Contracts - On Chain Contract Calls with the Collatz sequence",
            "description": 'Using <span class="code">sp.contract</span>, <span class="code">sp.transfer</span>, <span class="code">sp.self</span>, <span class="code">sp.self_entry_point</span>.',
        },
        {
            "fileName": "fixed_precision.py",
            "name": "Fixed precision computations",
            "description": "Example of fixed precision computation (log function) in SmartPy.",
        },
        {
            "fileName": "testHashFunctions.py",
            "name": "Hash Functions",
            "description": 'Using <span class="code">sp.blake2b</span>, <span class="code">sp.sha256</span>, <span class="code">sp.sha512</span>.',
        },
        {
            "fileName": "bakingSwap.py",
            "name": "Key hashes - Baking Swap",
            "description": 'Use of <span class="code">sp.set_delegate</span>, <span class="code">sp.sender</span>, <span class="code">sp.now</span>, <span class="code">sp.amount</span>.',
        },
        {
            "fileName": "lambdas.py",
            "name": "Lambdas",
            "description": "Lambdas in SmartPy.",
        },
        {
            "fileName": "testLists.py",
            "name": "Lists",
            "description": "Creation, iteration, construction from maps and sets, ranges.",
        },
        {
            "fileName": "test_maps.py",
            "name": "Maps",
            "description": "Misc operations on maps.",
        },
        {
            "fileName": "sapling.py",
            "name": "Sapling",
            "description": 'Simple example <span class="code">sp.sapling_verify_update</span>, <span class="code">sp.TSaplingState</span>, <span class="code">sp.TSaplingTransaction</span>.',
        },
        {
            "fileName": "sapling2.py",
            "name": "Sapling - more advanced example",
            "description": "Shield token example.",
        },
        {
            "fileName": "stringManipulations.py",
            "name": "Strings and Bytes",
            "description": 'Using <span class="code">sp.len</span>, <span class="code">+</span>, <span class="code">sp.concat</span>, <span class="code">e.slice(.., ..)</span>.',
        },
        {
            "fileName": "test_ticket.py",
            "name": "Tickets",
            "description": 'Using <span class="code">sp.TTicket</span>, <span class="code">sp.ticket</span>, <span class="code">sp.read_ticket</span>, <span class="code">sp.split_ticket</span>, <span class="code">sp.join_tickets</span>.',
        },
        {
            "fileName": "testTimestamp.py",
            "name": "Timestamps",
            "description": 'Using <span class="code">sp.now</span>, <span class="code">sp.timestamp</span>, <span class="code">(..).add_seconds</span> and <span class="code">-</span>.',
        },
        {
            "fileName": "testVariant.py",
            "name": "Variants, Options and Enums",
            "description": 'Using <span class="code">sp.is_variant</span>, <span class="code">sp.open_variant</span>, <span class="code">sp.is_some</span>, <span class="code">sp.open_some</span>, <span class="code">sp.match</span>.',
        },
        {
            "fileName": "testCheckSignature.py",
            "name": "Signatures",
            "description": 'Using <span class="code">sp.check_signature</span>.',
        },
    ],
    "Misc Features": [
        {
            "fileName": "syntax.py",
            "name": "Syntactic Constructions",
            "description": "Several syntax examples.",
        },
        {
            "fileName": "testDiv.py",
            "name": "Euclidean Division with sp.ediv",
            "description": 'Variations around <span class="code">sp.ediv</span>.',
        },
        {
            "fileName": "init_type_only.py",
            "name": "Init Type Only",
            "description": "Example without specifying the initial storage.",
        },
        {
            "fileName": "layout.py",
            "name": "Layouts of records and variants",
            "description": 'Changing the layouts of data types <span class="code">sp.set_record_layout</span>, <span class="code">sp.set_variant_layout</span>, <span class="code">sp.set_type_record_layout</span> and <span class="code">sp.set_type_variant_layout</span>.',
        },
        {
            "fileName": "lazy_entry_points.py",
            "name": "Upgradable and Lazy Entry Points",
            "description": "Entry points that can be upgraded and are loaded on-demand.",
        },
        {
            "fileName": "lazy.py",
            "name": "Lazy Strings",
            "description": "Big map to reduce gas usage.",
        },
        {
            "fileName": "metadata.py",
            "name": "Metadata",
            "description": "Defining metadata for a contract.",
        },
        {
            "fileName": "inlineMichelson.py",
            "name": "Inline Michelson",
            "description": "Direct inlining of Michelson code in SmartPy.",
        },
        {
            "fileName": "test_inheritance.py",
            "name": "Inheritance ",
            "description": "Various ways to inherit from another contract.",
        },
        {
            "fileName": "checkLanguage.py",
            "name": "Check Language Constructions",
            "description": "Many computations compared between pure Python and SmartPy.",
        },
        {
            "fileName": "decompilation.py",
            "name": "Decompilation Test",
            "description": "A very simple toy example to show how decompilation can work in SmartPy thanks to its meta-programming capabilities.",
        },
    ],
    "Token Contracts": [
        {
            "fileName": "FA1.2.py",
            "name": "FA1.2: Fungible Assets",
            "description": 'FA1.2 refers to an ERC20-like fungible token standard for Tezos. Proposed in <a href="https://gitlab.com/tzip/tzip/blob/master/proposals/tzip-7/tzip-7.md" target="_blank">TZIP-7</a>.',
        },
        {
            "fileName": "FA2.py",
            "name": "FA2: Fungible, Non-fungible, Multiple or Single Assets",
            "description": 'FA2 exposes a unified token contract interface, supporting a wide range of token types and implementations. Proposed in <a href="https://gitlab.com/tzip/tzip/blob/master/proposals/tzip-12/tzip-12.md" target="_blank">TZIP-12</a>.<br/>More documentation on how to use the FA2 contract can be found in <a href="https://smartpy.io/docs/guides/FA/FA2" target="_blank">our guide</a>',
        },
        {
            "fileName": "oracle.py",
            "name": "Chainlink Oracles",
            "description": "Building Chainlink oracles on Tezos - still experimental",
        },
    ],
    "Simple Examples": [
        {
            "fileName": "storeValue.py",
            "name": "Store Value",
            "description": "Store some data in the storage of a contract and change its value by calling its entry points.",
        },
        {
            "name": "Calculator",
            "fileName": "calculator.py",
            "description": "A simple calculator on the blockchain.",
        },
        {
            "fileName": "worldCalculator.py",
            "name": "World Calculator",
            "description": "A simple expression calculator on the blockchain (with parsing and pretty-printing).",
        },
        {
            "fileName": "fifo.py",
            "name": "Fifo",
            "description": "Contracts storing user defined first-in first-out data structures.",
        },
    ],
    "Protocols": [
        {
            "fileName": "atomicSwap.py",
            "name": "Atomic Swap",
            "description": "A simple, and naive, atomic swap contract.",
        },
        {
            "fileName": "escrow.py",
            "name": "Escrow",
            "description": "A simple escrow contract.",
        },
        {
            "fileName": "admin_multisig.py",
            "name": "Admin Multisig",
            "description": "A generic multisig to administrate other contracts.",
        },
        {
            "fileName": "multisig.py",
            "name": "Multisig",
            "description": "A complex contract handling several multisig sub-contracts, each have several groups of several participants with extensive parametrization.",
        },
        {
            "fileName": "stateChannels.py",
            "name": "State Channels (obsolete version)",
            "description": "A contract transforming a simple game into a state channel for this game.",
        },
    ],
    "State Channels": [
        {
            "fileName": "state_channel_games/game_platform.py",
            "name": "Game platform",
            "description": 'State channel based game platform. A complete guide can be found in <a href="https://smartpy.io/docs/guides/state_channels/overview" target="_blank">our guide</a>.',
        },
        {
            "fileName": "state_channel_games/game_tester.py",
            "name": "Game tester",
            "description": "Small contract to test game models.",
        },
        {
            "fileName": "state_channel_games/model_wrap.py",
            "name": "Game wrapper",
            "description": "Helper to prepare models for contracts.",
        },
        {
            "fileName": "state_channel_games/types.py",
            "name": "Game types",
            "description": "Type definitions for games.",
        },
        {
            "fileName": "state_channel_games/models/head_tail.py",
            "name": "Game: Head and Tail model",
            "description": "Game model for head and tail.",
        },
        {
            "fileName": "state_channel_games/models/nim.py",
            "name": "Game: Nim model",
            "description": "Game model for nim.",
        },
        {
            "fileName": "state_channel_games/models/tictactoe.py",
            "name": "Game: tic-tac-toe model",
            "description": "Game model for tic-tac-toe.",
        },
        {
            "fileName": "state_channel_games/models/transfer.py",
            "name": "Game: transfer model",
            "description": "Very simple model, transfer only.",
        },
    ],
    "Small Games": [
        {
            "fileName": "chess.py",
            "name": "Chess game",
            "description": "Example template with moves for a few pieces.",
        },
        {
            "fileName": "game_of_life.py",
            "name": "Game of Life",
            "description": "Example template for a game of life simulator.",
        },
        {
            "fileName": "jingleBells.py",
            "name": "Jingle Bells",
            "description": "A minimalistic contract to sing Jingle Bells. Dashing through the snow, ...",
        },
        {
            "fileName": "minikitties.py",
            "name": "Mini Kitties",
            "description": "Small example freely inspired by crypto-kitties",
        },
        {
            "fileName": "nim.py",
            "name": "Nim game",
            "description": """
            Implementation of a Nim game (wikipedia <a href="https://en.wikipedia.org/wiki/Nim" target="_blank">page<a>).
            <br/>Use of arrays.
            <br/>One contract handles one game.
            """,
        },
        {
            "fileName": "nimLift.py",
            "name": "Nim game repository",
            "description": """
            Implementation of a Nim game (wikipedia <a href='https://en.wikipedia.org/wiki/Nim' target="_blank">page</a>).
            <br/>One contract can handle many games in parallel.
            """,
        },
        {
            "fileName": "tictactoe.py",
            "name": "TicTacToe game",
            "description": "A simple TicTacToe game showing many regular concepts for simple games.",
        },
        {
            "fileName": "tictactoeFactory.py",
            "name": "TicTacToe game factory",
            "description": "A factory to handle several simple TicTacToe games showing many regular concepts for simple games.",
        },
    ],
}
