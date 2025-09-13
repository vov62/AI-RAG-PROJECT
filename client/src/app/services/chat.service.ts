import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal, WritableSignal } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class ChatService {

    http = inject(HttpClient)
    chatHistory = signal<{ user: string, bot: string }[]>([]);
    private baseUrl: string = 'http://127.0.0.1:5000/api';



    postquery(body: string) {
        return this.http.post(`${this.baseUrl}/query`, ({ body }))
    }


    addToHistory(userInput: string, aiResponse: string) {
        this.chatHistory.update(history => [
            ...history,
            { user: userInput, bot: aiResponse }
        ],)
        return this.chatHistory
    }

    getHistory() {
        return this.chatHistory;
    }

}
