async function loadAndRenderOutput() {
    try {
        const response = await fetch(`./output.json?t=${Date.now()}`, {
            cache: "no-store"
        });
        if (!response.ok) {
            throw new Error('output.json の取得に失敗しました。');
        }
        const data = await response.json();

        // 1. 中央ペインに全体のサンプルコードを表示
        document.getElementById('code-display').textContent = data.sample_code;

        const apis = data.apis;
        // ▼ HTML側のID（radio-tab-container）と一致させる
        const tabsContainer = document.getElementById('radio-tab-container');
        tabsContainer.innerHTML = "";

        if (!apis || apis.length === 0) {
            document.getElementById('api-detail-container').textContent = "API情報はありません。";
            return;
        }

        // 2. 配列の要素数に応じてタブ（ラジオボタン風）を動的生成
        apis.forEach((api, index) => {
            const label = document.createElement('label');
            label.style.cursor = "pointer";
            label.style.padding = "6px 12px";
            label.style.border = "1px solid #007bff";
            label.style.borderRadius = "4px";
            label.style.backgroundColor = index === 0 ? "#007bff" : "#fff";
            label.style.color = index === 0 ? "#fff" : "#007bff";
            label.style.fontSize = "14px";
            label.style.userSelect = "none";

            const radio = document.createElement('input');
            radio.type = "radio";
            radio.name = "api-tab-group";
            radio.value = index;
            radio.checked = (index === 0);
            radio.style.display = "none";

            label.appendChild(radio);
            label.appendChild(document.createTextNode(api.api_name));

            // タブクリック時の処理
            label.addEventListener('click', () => {
                Array.from(tabsContainer.children).forEach(lbl => {
                    lbl.style.backgroundColor = "#fff";
                    lbl.style.color = "#007bff";
                });

                label.style.backgroundColor = "#007bff";
                label.style.color = "#fff";
                radio.checked = true;

                renderAPIDetails(api);
            });

            tabsContainer.appendChild(label);
        });

        // 3. 初期表示として最初のAPI詳細を描画
        renderAPIDetails(apis[0]);
    } catch (error) {
        console.error('データ読み込みエラー:', error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadAndRenderOutput();

    const sendButton = document.getElementById('send-button');

    if (!sendButton) {
        console.error("エラー: #send-button が見つかりません。");
        return;
    }

    sendButton.addEventListener('click', async (event) => {
        event.preventDefault();

        const inputElement = document.getElementById('query-input');
        const queryText = inputElement ? inputElement.value.trim() : "";

        if (!queryText) {
            console.log("入力が空です。");
            return;
        }

        console.log("送信するクエリ:", queryText);

        try {
            const resData = await sendQueryToServer(queryText);
            console.log("サーバー応答:", resData);

            // server.py 側で output.json が更新された後に再読み込みして描画
            await loadAndRenderOutput();
        } catch (error) {
            console.error("送信または更新エラー:", error);
        }
    });
});

function renderAPIDetails(api) {
    const endpointDisplay = document.getElementById('endpoint-display');
    const parametersDisplay = document.getElementById('parameters-display');

    if (api.endpoint) {
        endpointDisplay.textContent = `Endpoint: ${api.endpoint}`;
        endpointDisplay.style.display = "block";
    } else {
        endpointDisplay.style.display = "none";
    }

    parametersDisplay.textContent = api.parameters;
}

async function sendQueryToServer(queryText) {
    const response = await fetch("http://localhost:5000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryText }),
    });

    if (!response.ok) {
        throw new Error(`HTTPエラー: ${response.status}`);
    }

    return await response.json();
}