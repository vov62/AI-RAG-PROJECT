import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class ChatService {

    http = inject(HttpClient)
    chatHistory = signal<{ user: string, bot: string }[]>([]);


    addToHistory(userInput: string, aiResponse: string) {
        this.chatHistory.update(history => [
            ...history,
            { user: userInput, bot: aiResponse }
        ])
        return this.chatHistory
    }

    getHistory() {
        return this.chatHistory;
    }

}
