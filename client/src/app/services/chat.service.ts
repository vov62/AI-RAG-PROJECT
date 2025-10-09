import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { environment } from '../../environments/environment.prod';


@Injectable({
    providedIn: 'root'
})
export class ChatService {

    http = inject(HttpClient)
    chatHistory = signal<{ user: string, bot: string }[]>([]);
    // private baseUrl: string = 'http://127.0.0.1:5000/api';
    // פרודוקשיין
    private baseUrl = environment.apiUrl;


    // שליחת יוזר אינפוט
    postquery(body: any) {
        return this.http.post(`${this.baseUrl}/query`, body)
    }
    // ניסוח טקסט מחדש
    rephraseQuery(query: string) {
        return this.http.post(`${this.baseUrl}/rephrase`, { query });
    }

    // שליחת היסטוריה של הודעות לAI
    addToHistory(userInput: string, aiResponse: string) {
        this.chatHistory.update(history => [
            ...history,
            { user: userInput, bot: aiResponse },
        ]);
        this.saveHistoryToLocalStorage();
        return this.chatHistory
    }

    getHistory() {
        return this.chatHistory;
    }

    private saveHistoryToLocalStorage() {
        localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory()));
    }

    loadHistoryFromLocalStorage() {
        const savedHistory = localStorage.getItem("chatHistory");
        if (savedHistory) {
            this.chatHistory.set(JSON.parse(savedHistory));
        }
    }




}
