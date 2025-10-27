import { Commands } from '@tiptap/core';

declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    // Base commands that are always available

    run: () => ReturnType;

    // Extension-specific commands
    image: {
      setImage: (options: { src: string }) => ReturnType;
    };
    link: {
      setLink: (attributes: { href: string }) => ReturnType;
      unsetLink: () => ReturnType;
    };
    // youtube: {
    //   setYoutubeVideo: (options: {
    //     src: string;
    //     width?: string;
    //     height?: string;
    //   }) => ReturnType;
    // };
    bold: {
      toggleBold: () => ReturnType;
    };
    italic: {
      toggleItalic: () => ReturnType;
    };
    strike: {
      toggleStrike: () => ReturnType;
    };
    code: {
      toggleCode: () => ReturnType;
    };
    paragraph: {
      setParagraph: () => ReturnType;
    };
    heading: {
      toggleHeading: (attributes: { level: number }) => ReturnType;
    };
    bulletList: {
      toggleBulletList: () => ReturnType;
    };
    orderedList: {
      toggleOrderedList: () => ReturnType;
    };
    codeBlock: {
      toggleCodeBlock: () => ReturnType;
    };
    blockquote: {
      toggleBlockquote: () => ReturnType;
    };
    horizontalRule: {
      setHorizontalRule: () => ReturnType;
    };
    hardBreak: {
      setHardBreak: () => ReturnType;
    };
    history: {
      undo: () => ReturnType;
      redo: () => ReturnType;
    };
    color: {
      setColor: (color: string) => ReturnType;
    };
    table: {
      insertTable: (options: {
        rows: number;
        cols: number;
        withHeaderRow?: boolean;
      }) => ReturnType;
      addColumnBefore: () => ReturnType;
      addColumnAfter: () => ReturnType;
      deleteColumn: () => ReturnType;
      addRowBefore: () => ReturnType;
      addRowAfter: () => ReturnType;
      deleteRow: () => ReturnType;
      deleteTable: () => ReturnType;
      mergeCells: () => ReturnType;
      splitCell: () => ReturnType;
      toggleHeaderColumn: () => ReturnType;
      toggleHeaderRow: () => ReturnType;
      toggleHeaderCell: () => ReturnType;
      mergeOrSplit: () => ReturnType;
      setCellAttribute: (name: string, value: any) => ReturnType;
      fixTables: () => ReturnType;
      goToNextCell: () => ReturnType;
      goToPreviousCell: () => ReturnType;
    };
    textAlign: {
      setTextAlign: (
        align: 'left' | 'center' | 'right' | 'justify'
      ) => ReturnType;
    };
  }
}
